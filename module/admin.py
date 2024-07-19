from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Module)
admin.site.register(Lesson)
admin.site.register(Content)
admin.site.register(Section)
admin.site.register(Score)
admin.site.register(Word)
admin.site.register(CustomerRecording)