from django.urls import path
from .views import *

app_name = 'game'

urlpatterns = [
    path('', match_voice, name='matchvoice'),
    path('gameover/', gameover, name='gameover'),
]
