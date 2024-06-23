from django.urls import path
from .views import *

app_name = "modules"

urlpatterns = [    
    path("module/<pk>/", moduleSectionPage , name="module"),
    path('record_audio/', record_audio, name='record_audio'),
    path('upload_media/', upload_media, name='upload_media')

]