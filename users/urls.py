from django.contrib import admin
from django.urls import path
from .views import *

app_name = "users"

urlpatterns = [
    path('subscribe/', subscribe, name='subscribe'),
    path('success/', success, name='success'),
    path('cancel/', cancel, name='cancel'),
]
