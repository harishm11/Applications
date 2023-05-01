from .models import *
from django import forms



class feedbackpageform(forms.ModelForm):
    class Meta:
       model = feedbackpagemodel
       exclude =[]
       widgets = {
           'Username': forms.TextInput(attrs={'type':'hidden'})
       }