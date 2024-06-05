from django.shortcuts import render
from django.urls import resolve

# Create your views here.

def modules__view(request):
    current_url = resolve(request.path_info).url_name
    print(f"Current URL: {current_url}")  # Debugging line
    context = {
        'current_url': current_url,
    }
    return render(request, 'module.html', context)

