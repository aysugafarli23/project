from django import forms
from .models import ContactSubmission

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }
        
         
    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       
       for field in self.fields.values():
           field.widget.attrs['class'] = 'form-control'
