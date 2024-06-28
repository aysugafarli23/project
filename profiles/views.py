from django.shortcuts import render, redirect, get_object_or_404
from django.urls import resolve
from django.contrib import messages
from contact.forms import ContactForm  
from django.contrib.auth.decorators import login_required

# @login_required(login_url="account:login")
def profilePage(request):
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


    context = {
        'current_url': current_url,
        'form': form,
    }
    return render(request, "profile.html", context)
