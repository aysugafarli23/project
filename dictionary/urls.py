from django.urls import path
from .views import *

app_name = "dictionary"

urlpatterns = [
    path(f'search/', searchPage, name="search"),
]