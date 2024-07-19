from django.urls import path
from .views import *

app_name = "modules"

urlpatterns = [   
    path("<pk>/lessons/", lessonsPage , name="lessons"), 
    path("lessons/<pk>/", lessonSectionPage , name="lessons_section"),
    path('upload_media/', upload_media, name='upload_media'),
    path('words/', generate_speech, name='generate_speech'),
    path('record_audio/<int:word_id>/', record_audio, name='record_audio'),
    

]