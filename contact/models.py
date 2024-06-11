from django.db import models

class ContactSubmission(models.Model):
    name = models.CharField(max_length=100, verbose_name=("Name"))
    email = models.EmailField()
    subject = models.CharField(max_length=200, verbose_name=("Subject"), blank=True, null=True)
    message = models.TextField(max_length=200, verbose_name=("Message"))
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"
