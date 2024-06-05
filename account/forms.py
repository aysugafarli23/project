from django import forms

class Nativel(forms.Form):
    COMMON_LANGS = [
        ('es', 'Spanish'),
        ('hi', 'South Asian Languages (Hindi, Urdu, Nepali, Bengali, Punjabi, Telugu)'),
        ('zh', 'Chinese Languages (Mandarin, Cantonese, etc.)'),
        ('ja', 'Japanese'),
        ('ko', 'Korean'),
        ('pt', 'Portuguese Languages (Portuguese)'),
        ('sw', 'African Languages (Swahili)'),
        ('ar', 'Arabic'),
        ('fa', 'Persian'),
        ('other', 'Other')
    ]

    native_languages = forms.ChoiceField(
        choices=COMMON_LANGS,
        widget=forms.RadioSelect,
        label="Select your native language",
        required=False,
    )
