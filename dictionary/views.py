from django.shortcuts import render, redirect
from django.urls import resolve
from django.contrib import messages
from contact.forms import ContactForm  
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url="login")
def dictPage(request):
     # Contact form logic
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your message.')
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        form = ContactForm()
    current_url = resolve(request.path_info).url_name
    context = {
        'current_url': current_url,
        'form': form,  # Include the form in the context
    }
    
    # Render module.html with the context including the form
    return render(request, 'dict.html', context)
