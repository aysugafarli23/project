from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.views import LoginView,  PasswordChangeView
from .forms import *
from contact.forms import ContactForm
from django.contrib.auth.decorators import login_required  
from django.urls import reverse_lazy, resolve
from django.conf import settings
from djstripe.models import Customer, Product, Price, Plan as StripePlan
import stripe
from .models import *
from formtools.wizard.views import SessionWizardView
from django.http import  HttpResponse,HttpResponseRedirect
from django.db.utils import IntegrityError



class CustomRegisterView(SessionWizardView):
    form_list = [RegisterForm, CustomDetailForm, SubscriptionPlanForm]
    template_name = 'register.html'

    
    def done(self, form_list, **kwargs):
        register_form = form_list[0]
        custom_detail_form = form_list[1]
        subscription_plan_form = form_list[2]

        # Extract data from the form
        username = register_form.cleaned_data['username']
        password = register_form.cleaned_data['password']

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already exists. Please choose another username.")

        try:
            # Create the user
            new_user = User(username=username)
            new_user.set_password(password)
            new_user.save()

            # Save the register form and link it to the user
            register = register_form.save(commit=False)
            register.user = new_user
            register.save()

            # Save the custom detail form and link it to the register
            custom_detail = custom_detail_form.save(commit=False)
            custom_detail.register = register
            custom_detail.save()
            
            # Save the subscription plan form and link it to the user
            subscription_plan = subscription_plan_form.save(commit=False)
            subscription_plan.user = new_user
            subscription_plan.save()
            
           # Create a Stripe Checkout session
            price_id = subscription_plan.price_id
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price': price_id,
                    'quantity': 1,
                }],
                mode='subscription',
                success_url='http://127.0.0.1:8000/users/success/',
                cancel_url='http://127.0.0.1:8000/users/cancel/',
            )

            # Redirect to the payment link
            return HttpResponseRedirect(checkout_session.url)

        except IntegrityError:
            return HttpResponse("There was an error creating the user. Please try again.")
        
        
# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)
    

@login_required
def profile(request):
    # Handle ContactForm submission
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your message.')
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        form = ContactForm()
    current_url = resolve(request.path_info).url_name



    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
    
    context = {
        'current_url': current_url,
        'form': form,
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'profile.html', context)
    


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('profile')
   
    
#Stripe configuration
stripe.api_key = settings.STRIPE_LIVE_SECRET_KEY

def subscribe(request):
    if request.method == 'POST':
        plan_id = request.POST.get('plan_id')
        price = Price.objects.get(id=plan_id)
            
        try:
            customer, created = Customer.get_or_create(subscriber=request.user)

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price': price.id,
                        'quantity': 1,
                    },
                ],
                mode='subscription',
                customer=customer.id,
                success_url='http://127.0.0.1:8000/users/success/',
                cancel_url='http://127.0.0.1:8000/users/cancel/',
            )
            return redirect(checkout_session.url)
        except Exception as e:
            return render(request, 'error.html', {'message': str(e)})

    prices = Price.objects.all()
    return render(request, 'subscribe.html', {'prices': prices})


def success(request):
    # Handle the success callback from Stripe
    return render(request, 'success.html')

def cancel(request):
    # Handle the cancellation callback from Stripe
    return render(request, 'cancel.html')

# On CMD:
# python manage.py djstripe_sync_models Price
# python manage.py djstripe_sync_models Plan
