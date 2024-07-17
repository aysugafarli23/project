from django.urls import path
from .views import *

app_name = "modules"

urlpatterns = [   
    path("<pk>/lessons/", lessonsPage , name="lessons"), 
    path("lessons/<pk>/", lessonSectionPage , name="lessons_section"),
    path('record_audio/', record_audio, name='record_audio'),
    path('upload_media/', upload_media, name='upload_media')

]