from django.shortcuts import render
from django.urls import resolve

# Create your views here.
def profilePage(request):
    current_url = resolve(request.path_info).url_name
    context = {
        'current_url': current_url,
    }
    return render(request, 'profile.html', context)