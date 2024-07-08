from django.db import models
from django.contrib.auth.models import  AbstractUser
from PIL import Image

# Create your models here.
class User(AbstractUser):
    
    class People(models.TextChoices):
        H = 'H', 'have told me that I have a strong accent.'
        O = 'O',  'often ask me to repeat what I said'
        S = 'S', 'speak too fast, and I have a hard time understanding.'
        
    class Method(models.TextChoices):
        B = 'B', 'Be better at my current job and get paid more'
        F = 'F', 'Find a new job'
        I = 'I', 'Improve my networking and relationships'
        T = 'T', 'To get better immersed in the American culture'
        
    class USA(models.TextChoices):
        Y = 'Y', 'Yes'
        N = 'N', 'No'

    class Speak(models.TextChoices):
        P80 = '80', '80% of the time or more'
        P50 = '50', 'about 50% of the time'
        P10 = '10', '10% of the time or less'

    class Minute(models.TextChoices):
        M5 = '5', '5-10 mins'
        M15 = '15', '15-20 minute'
        M30 = '30', '30 mins'
        MORE = 'more', 'More than that'
      
    email = models.EmailField()    
    nativel = models.CharField(max_length=100)
    people = models.CharField(max_length=1, choices=People.choices)
    method = models.CharField(max_length=1, choices=Method.choices)
    usa = models.CharField(max_length=1, choices=USA.choices)
    speak = models.CharField(max_length=2, choices=Speak.choices)
    minute = models.CharField(max_length=4, choices=Minute.choices)


# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username
    
    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)
     
     