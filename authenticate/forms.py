from .models import *
from django import forms


class feedbackpageform(forms.ModelForm):
    class Meta:
        model = Feedbackmodel
        exclude = []
        widgets = {
            'Username': forms.TextInput(attrs={'type': 'hidden'})
        }
