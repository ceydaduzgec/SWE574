from django import forms
from .models import WebAnnotation

class WebAnnotationForm(forms.ModelForm):
    class Meta:
        model = WebAnnotation
        fields = ['target', 'body']