from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from djstripe.models import *
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class RegisterForm(forms.ModelForm):
    
    class Meta:
        model = Register
        fields = ['username', 'password', 'password_confirm', 'email']
        widgets = {
            'password': forms.PasswordInput(attrs={'data-toggle':'password'}),
            'password_confirm': forms.PasswordInput(attrs={'data-toggle':'password'})
        }
        
    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) <= 3:
            raise forms.ValidationError("Username is too short")
        return username 
        


class CustomDetailForm(forms.ModelForm): 
    # fields we want to include and customize in our form
    nativel = forms.ChoiceField(choices=[], label="Native language")

    class Meta:
        model = CustomDetail
        fields = ['nativel', 'situation', 'method','usa','speak', 'minute']
        widgets = {
            'situation': forms.RadioSelect,
            'method': forms.RadioSelect,
            'usa': forms.RadioSelect,
            'speak': forms.RadioSelect,
            'minute': forms.RadioSelect,
        }
        
    def __init__(self, *args, **kwargs):
        super(CustomDetailForm, self).__init__(*args, **kwargs)
        self.fields['nativel'].choices = self.get_nativel_choices()
        # Set choices without the blank option
        self.fields['situation'].choices = [(choice.value, choice.label) for choice in CustomDetail.Situation]
        self.fields['method'].choices = [(choice.value, choice.label) for choice in CustomDetail.Method]
        self.fields['usa'].choices = [(choice.value, choice.label) for choice in CustomDetail.USA]
        self.fields['speak'].choices = [(choice.value, choice.label) for choice in CustomDetail.Speak]
        self.fields['minute'].choices = [(choice.value, choice.label) for choice in CustomDetail.Minute]

     
    def get_nativel_choices(self):
        with open('users/languages.txt') as f:
            nativels = f.read().splitlines()
        return [(nativel, nativel) for nativel in nativels]
 
 
class SubscriptionPlanForm(forms.ModelForm):
    plan = forms.ChoiceField(choices=[], label="Subscription Plan")

    class Meta:
        model = SubscriptionPlan
        fields = ['plan']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['plan'].choices = self.get_price_choices()

    def get_price_choices(self):
        prices = Price.objects.filter(active=True).order_by('unit_amount')
        choices = []
        for price in prices:
            interval = price.recurring["interval"]
            display_name = f"{price.unit_amount / 100:.2f} {price.currency.upper()}/{interval.capitalize()} for {price.product.name}"
            choices.append((price.id, display_name))
        return choices

    def save(self, commit=True):
        subscription_plan = super().save(commit=False)
        subscription_plan.price_id = self.cleaned_data['plan']
        if commit:
            subscription_plan.save()
        return subscription_plan

    
    # def save(self, commit=True):
    #     """ Hash users's password on save """
    #     user = super().save(commit=False)
    #     user.set_password(self.cleaned_data['password'])
    #     if commit:
    #         user.save()
    #     return user
        

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
    class Gender(models.TextChoices):
        M = 'Male', 'Male'
        F = 'Female', 'Female'
        O = 'Other', 'Other'
        
        
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}), label="", initial='../media/default.png')
    gender = forms.ChoiceField(label="Gender", choices=Gender.choices,  widget=forms.RadioSelect(attrs={'class': 'form-control'}))
    nativel = forms.ChoiceField(choices=[])
       
    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        self.fields['nativel'].choices = self.get_nativel_choices()
        # Set choices without the blank option
     
    def get_nativel_choices(self):
        with open('users/languages.txt') as f:
            nativels = f.read().splitlines()
        return [(nativel, nativel) for nativel in nativels]
    

    class Meta:
        model = Profile
        fields = ['avatar', 'gender', 'nativel']
        
   
        