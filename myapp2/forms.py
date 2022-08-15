from django.forms import ModelForm
from .models import *


class driverForm(ModelForm):
    class Meta:
       model = driverModel
       exclude =[]

class vehicleForm(ModelForm):
    class Meta:
       model = vehicleModel
       exclude =[]


class incidentForm(ModelForm):
    class Meta:
       model = incidentModel
       exclude =[]


class policyForm(ModelForm):
    class Meta:
       model = policyModel
       exclude =['quoteNumber','policyNumber']