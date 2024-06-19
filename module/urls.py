from django.urls import path
from .views import *

app_name = "modules"

urlpatterns = [    
    path("module/<pk>/", moduleSectionPage , name="module"),
]