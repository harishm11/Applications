from django.forms import ModelForm
from .models import *

# Create the form class.
class inputtdataForm(ModelForm):
    class Meta:
       model = inputtdata
       fields = ['zipcode',]