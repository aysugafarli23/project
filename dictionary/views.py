from django.shortcuts import render
from django.urls import resolve

# Create your views here.
def dictPage(request):
    current_url = resolve(request.path_info).url_name
    context = {
        'current_url': current_url,
    }
    return render(request, 'dict.html', context)

def searchPage(request):
    current_url = resolve(request.path_info).url_name
    context = {
        'current_url': current_url,
    }
    return render(request, 'search.html', context)