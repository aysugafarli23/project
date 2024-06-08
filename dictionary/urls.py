from django.urls import path, include
from .views import *

app_name = "dictionary"

urlpatterns = [
    path('search/', searchPage, name="search"),
]