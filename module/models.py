# myapp/models.py
from django.db import models
from django.contrib.auth.models import User



class Module(models.Model):
    module_title = models.CharField(max_length=200)
    module_image = models.FileField(upload_to="module_images/", blank=True, null=True)

    def __str__(self):
        return self.module_title

class Lesson(models.Model):
    lesson_module = models.ForeignKey(Module, related_name='lessons', on_delete=models.CASCADE)
    lesson_title = models.CharField(max_length=255)
    lesson_image = models.FileField(upload_to="lesson_images/", blank=True, null=True)

    def __str__(self):
        return f"{self.lesson_module.module_title} - {self.lesson_title}"

class Section(models.Model):
    section_lesson = models.ForeignKey(Lesson, related_name='sections', on_delete=models.CASCADE)
    section_title = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.section_lesson.lesson_title} - {self.section_title}"

class Content(models.Model):
    content_section = models.ForeignKey(Section, related_name='contents', on_delete=models.CASCADE)
    content_title = models.CharField(max_length=200)
    body = models.TextField(blank=True, null=True)
    content_image = models.FileField(upload_to='content_images/', blank=True, null=True)
    video_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.content_title

class Word(models.Model):
    text = models.TextField()
    audio_file_alloy = models.FileField(upload_to='words_audio/', blank=True, null=True)
    audio_file_nova = models.FileField(upload_to='words_audio/', blank=True, null=True)
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='words')
    
    def __str__(self):
       return f"{self.id} - {self.text}"

class CustomerRecording(models.Model):
    audio_file = models.FileField(upload_to='customer_recordings/')
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.word.text} - {self.created_at}"
