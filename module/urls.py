from django.urls import path
from .views import *

app_name = "modules"

urlpatterns = [   
    path("<pk>/lessons/", lessonsPage , name="lessons"), 
    path("lessons/<pk>/", lessonSectionPage , name="lessons_section"),
    path('words/', generate_speech, name='generate_speech'),
    path('record_audio/<int:word_id>/', WordView.as_view(), name='record_audio'),
    path('compare_audio/<int:word_id>/', compare_audio, name='compare_audio'),
]