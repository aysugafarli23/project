from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile
from djstripe.models import *

class RegisterForm(UserCreationForm):
    PEOPLE_CHOICES = [
        ('H', 'have told me that I have a strong accent.'),
        ('O', 'often ask me to repeat what I said'),
        ('S', 'speak too fast, and I have a hard time understanding.'),
    ]
    METHOD_CHOICES = [
        ('B', 'Be better at my current job and get paid more'),
        ('F', 'Find a new job'),
        ('I', 'Improve my networking and relationships'),
        ('T', 'To get better immersed in the American culture')
    ]
    USA_CHOICES = [
        ('Y', 'Yes'),
        ('N', 'No')
    ]
    SPEAK_CHOICES = [
        ('1', '80% of the time or more'),
        ('2', 'about 50% of the time'),
        ('3', '10% of the time or less')
    ]
    MINUTE_CHOICES = [
        ('1', '5-10 mins'),
        ('2', '15-20 minute'),
        ('3', '30 mins'),
        ('4', 'More than that'),
    ]
    
    # fields we want to include and customize in our form
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    username = forms.CharField(max_length=100)
    email = forms.EmailField( )
    password1 = forms.CharField(max_length=50,  widget=forms.PasswordInput(attrs={'data-toggle': 'password', 'id': 'password',}))
    password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'data-toggle': 'password','id': 'password',}))
    nativel = forms.ChoiceField(choices=[])
    people = forms.ChoiceField(choices=PEOPLE_CHOICES, widget=forms.RadioSelect(attrs={'class': 'form-check-input'}))
    method = forms.ChoiceField(choices=METHOD_CHOICES, widget=forms.RadioSelect(attrs={'class': 'form-check-input'}))
    usa = forms.ChoiceField(choices=USA_CHOICES, widget=forms.RadioSelect(attrs={'class': 'forms-check-input'}))
    speak = forms.ChoiceField(choices=SPEAK_CHOICES, widget=forms.RadioSelect(attrs={'class': 'form-check-input'}))
    minute = forms.ChoiceField(choices=MINUTE_CHOICES, widget=forms.RadioSelect(attrs={'class': 'form-check-input'}))
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'nativel', 'people', 'method','usa','speak', 'minute']
        
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['nativel'].choices = self.get_nativel_choices()
        for field in self.fields.values():
           field.widget.attrs['class'] = 'form-control '
           

    def get_nativel_choices(self):
        with open('users/languages.txt') as f:
            nativels = f.read().splitlines()
        return [(nativel, nativel) for nativel in nativels]
        

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100, required=True,widget=forms.TextInput(attrs={'placeholder': 'Username','class': 'form-control',}))
    password = forms.CharField(max_length=50, required=True,widget=forms.PasswordInput(attrs={'placeholder': 'Password','class': 'form-control','data-toggle': 'password','id': 'password','name': 'password',}))
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']
        
class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']
   
        