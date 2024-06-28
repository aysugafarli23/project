"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views  
from users.forms import LoginForm
from users.views import *
from module.views import *
from dictionary.views import *
from profiles.views import *
from contact.views import *



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', modulesPage, name = "contact"),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('modules/', modulesPage, name="modules"),
    path('modules/', include("module.urls")),
    path('modules-api/', include("module.api.urls"), name="modules-api"),
    path('dictionary/', dictPage, name = "dictionary"),
    path('dictionary/', include("dictionary.urls")),
    path('profile/', profilePage, name="profile"),
    path('profile/', include('profiles.urls')),
    path('contact/', include('contact.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)