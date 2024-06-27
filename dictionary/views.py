from django.shortcuts import render, redirect
from django.urls import resolve
from django.contrib import messages
from contact.forms import ContactForm  
# Create your views here.

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



def searchPage(request):
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
    query = ''  # Reset the query to an empty string

    if 'q' in request.GET:
        query = request.GET['q'].strip()

    context = {
        'current_url': current_url,
        'form': form,
        'query': query,
    }

    return render(request, 'search.html', context)