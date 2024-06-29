# myapp/models.py
from django.db import models
from django.contrib.auth.models import User

class Module(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.title}"
    
class Lesson(models.Model):
    module = models.ForeignKey(Module, related_name='lessons', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="Lesson Images", blank=True, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.module.title} - {self.title}"

class Content(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='content_images/', blank=True, null=True)
    audio = models.FileField(upload_to='content_audio/', blank=True, null=True)
    audio_file = models.FileField(upload_to="recordings/", null=True, blank=True)
    video = models.FileField(upload_to='content_videos/', blank=True, null=True)
    user = models.ForeignKey(User, related_name='contents', on_delete=models.CASCADE, null=True)


    def __str__(self):
        return f"{self.title}"

class Section(models.Model):
    title = models.CharField(max_length=200)
    lesson = models.ManyToManyField(Module, related_name='sections')
    contents = models.ManyToManyField(Content, related_name='sections')

    def __str__(self):
        return f"{self.title}"

class Score(models.Model):
    user = models.ForeignKey(User, related_name='scores', on_delete=models.CASCADE)
    content = models.ForeignKey(Content, related_name='scores', on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user} - {self.content} - {self.score}'
