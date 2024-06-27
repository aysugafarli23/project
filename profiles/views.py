from django.shortcuts import render, redirect
from django.urls import resolve
from django.contrib import messages
from contact.forms import ContactForm  
from .forms import ProfileForm
# Create your views here.


#Contact Form
# @login_required(login_url="account:login")
def profilePage(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your message.')
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        form = ContactForm()
    current_url = resolve(request.path_info).url_name
    
#Profile Form on Dashboard    
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            # Process the form data
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            country = form.cleaned_data['country']
            gender = form.cleaned_data['gender']
            age = form.cleaned_data['age']
            # Save the data to the database or perform other actions
            return redirect('success_url')  # Redirect to a success page or another view
    else:
        form = ProfileForm()
    context = {
        'current_url': current_url,
        'form': form, 
        'user': request.user
    }
    
    return render(request, 'profile.html', context)

