from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile
from djstripe.models import *

class RegisterForm(UserCreationForm):
    # fields we want to include and customize in our form
    first_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name','class': 'form-control',}))
    last_name = forms.CharField(max_length=100,required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control',}))
    username = forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'placeholder': 'Username','class': 'form-control',}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Email','class': 'form-control',}))
    password1 = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password','class': 'form-control','data-toggle': 'password', 'id': 'password',}))
    password2 = forms.CharField(max_length=50, required=True,widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password','class': 'form-control','data-toggle': 'password','id': 'password',}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        

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
   
        
#Stripe Subscription
PLACEHOLDER_PLAN_CHOICES = [
    ('price_1NxoPmEe6AtWy3dPwOwFqHnG', 'Free Plan'),
    ('price_1NxoPHEe6AtWy3dPOkj2cVfj', 'Pro Plan'),
]

class SubscriptionForm(forms.Form):
    plan = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['plan'].choices = [
            ('', '- Select a plan -')
        ] + [(pk, label) for pk, label in PLACEHOLDER_PLAN_CHOICES]

    def clean(self):
        cleaned_data = super().clean()
        plan_pk = cleaned_data.get("plan")
        if plan_pk and not Price.objects.filter(product__nickname=plan_pk).exists():
            raise forms.ValidationError('Selected plan cannot be processed.')
        return cleaned_data