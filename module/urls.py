from django.urls import path
from .views import *
from module.game.views import match_voice, gameover

app_name = "modules"

urlpatterns = [   
    path("<pk>/lessons/", lessonsPage , name="lessons"), 
    path('words/', generate_speech, name='generate_speech'),
    path('record_audio/<int:word_id>/', WordView.as_view(), name='record_audio'),
    path('compare_audio/<int:word_id>/', compare_audio, name='compare_audio'),
    # path('speech_recognition/<int:word_id>/', SpeechToTextView.as_view(), name='speech_recognition'),
    # path('assess_audio/<int:word_id>/', assess_audio, name='assess_audio'),
    path('game/', match_voice, name='matchvoice'),
    path('game/gameover/', gameover, name='gameover'),
    # path('assess_record_audio/<int:word_id>/', SpeechToTextView.as_view(), name='assess_record_audio'),
    # path('assess_audio/<int:word_id>/', AssessCompareAudioView.as_view(), name='assess_audio'),
]
