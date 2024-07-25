from django.contrib import admin
from .models import *
from .game.models import *

# Register your models here.
admin.site.register(Module)
admin.site.register(Lesson)
admin.site.register(Content)
admin.site.register(Section)
admin.site.register(Word)
admin.site.register(CustomerRecording)
admin.site.register(MatchingGameWord)
admin.site.register(Score)