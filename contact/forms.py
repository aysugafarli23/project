from django import forms
from .models import ContactSubmission

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 6}),
        }
        
         
    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       placeholders = {
                        'name': 'Name*',
                        'email': 'Email*',
                        'subject': 'Subject',
                        'message': 'How can we help you?'
                    }
  
       for field_name, field in self.fields.items():
           field.widget.attrs['class'] = 'form-control'
           field.label = ''
           if field_name in placeholders:
               field.widget.attrs['placeholder'] = placeholders[field_name]
