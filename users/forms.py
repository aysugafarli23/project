from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User, Profile
from djstripe.models import *
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class RegisterForm(forms.ModelForm): 
    # fields we want to include and customize in our form
    nativel = forms.ChoiceField(choices=[])
    people = forms.ChoiceField(choices=User.People.choices)
    method = forms.ChoiceField(choices=User.Method.choices)
    usa = forms.ChoiceField(choices=User.USA.choices)
    speak = forms.ChoiceField(choices=User.Speak.choices)
    minute = forms.ChoiceField(choices=User.Minute.choices)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'nativel', 'people', 'method','usa','speak', 'minute']
        widgets = {
            'password': forms.PasswordInput(attrs={'data-toggle':'password'}),
        }
        
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['nativel'].choices = self.get_nativel_choices()
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

        self.helper = FormHelper(self)
        # self.helper.form_action = reverse_lazy('login')
        self.helper.form_id = 'register-form'
        self.helper.attrs = {
            'hx-post': reverse_lazy('login'),
            'hx-target': '#register-form',
            'hx-swap': 'outerHTML'
        }
        self.helper.add_input(Submit('submit', 'Submit'))
      
     
    def get_nativel_choices(self):
        with open('users/languages.txt') as f:
            nativels = f.read().splitlines()
        return [(nativel, nativel) for nativel in nativels]
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) <= 3:
            raise forms.ValidationError("Username is too short")
        return username 
        
    
    def save(self, commit=True):
        """ Hash users's password on save """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
        

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
   
        