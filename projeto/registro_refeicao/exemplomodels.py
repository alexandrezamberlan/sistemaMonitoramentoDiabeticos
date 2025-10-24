# forms.py
from django import forms

class DictationForm(forms.Form):
    text_field = forms.CharField(widget=forms.Textarea, label='Texto')
