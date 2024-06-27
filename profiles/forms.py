# forms.py
from django import forms

# Read the list of countries from the file
with open('profiles/countries.txt', 'r') as file:
    countries__list = [(line.strip(), line.strip()) for line in file]
    
with open('profiles/languages.txt', 'r') as file:
    languages__list = [(line.strip(), line.strip()) for line in file]

class ProfileForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    country = forms.ChoiceField(choices=countries__list, required=True)
    gender = forms.ChoiceField(choices=[('male', 'Male'), ('female', 'Female'), ('others', 'Others')], required=True)
    language = forms.ChoiceField(choices=languages__list, required=True)
    age = forms.IntegerField(required=True)
