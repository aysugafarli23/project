from django.shortcuts import render
from django.urls import resolve
from contact.views import contact__view
# Create your views here.

def modulesPage(request):
    if request.method == 'POST':
        return contact__view(request)
    
    current_url = resolve(request.path_info).url_name
    context = {
        'current_url': current_url,
    }
    return render(request, 'module.html', context)

