from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.views import LoginView,  PasswordChangeView
from .forms import *
from contact.forms import ContactForm
from django.contrib.auth.decorators import login_required  
from django.urls import reverse_lazy, resolve
import os
from django.conf import settings
from djstripe.models import Customer, Price, Product
import stripe
from .models import *

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'register.html'
    
    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='/')

        return render(request, self.template_name, {'form': form})
    

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


# stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

def subscribe(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            plan_name = form.cleaned_data['plan']
            plan = Plan.objects.get(name=plan_name)

            try:
                customer, created = Customer.get_or_create(subscriber=request.user)

                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[
                        {
                            'price': plan.stripe_price_id,
                            'quantity': 1,
                        },
                    ],
                    mode='subscription',
                    customer=customer.id,
                    success_url='http://127.0.0.1:8000/success/',
                    cancel_url='http://127.0.0.1:8000/cancel/',
                )
                return redirect(checkout_session.url)
            except Exception as e:
                return render(request, 'error.html', {'message': str(e)})
    else:
        form = SubscriptionForm()
    return render(request, 'subscribe.html', {'form': form})

def success(request):
    # Handle the success callback from Stripe
    return render(request, 'success.html')

def cancel(request):
    # Handle the cancellation callback from Stripe
    return render(request, 'cancel.html')


def plans(request):
    # Fetch all products and their prices from the local database
    products = Product.objects.all()
    return render(request, 'plans.html', {'products': products})
