from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm

def contact__view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  
            messages.success(request, 'Thank you for your message.')
            return redirect('modules') 
    else:
        form = ContactForm()
    
    return render(request, 'base.html', {'form': form})
