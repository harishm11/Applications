from django.forms.models import modelform_factory
import json
from django import forms
from django.apps import apps
from django.db import models
state = apps.get_model('productconfigurator', 'state')
carrier = apps.get_model('productconfigurator', 'carrier')
product = apps.get_model('productconfigurator', 'product')


class ProductForm(forms.ModelForm):

    Carrier = forms.ModelChoiceField(
        queryset=carrier.objects.all(),
        label='Carrier'
    )
    StateCode = forms.ModelChoiceField(
        queryset=state.objects.all(),
        label='StateCode'
    )

    class Meta:
        model = product
        fields = '__all__'
        widgets = {
            'OpenBookStartDate': forms.DateInput(attrs={'type': 'date'}),
            'CloseBookEndDate': forms.DateInput(attrs={'type': 'date'}),
            'EffectiveDate': forms.DateInput(attrs={'type': 'date'}),
            'ExpiryDate': forms.DateInput(attrs={'type': 'date'}),
        }


FIELD_TYPES = [
    ('CharField', 'CharField'),
    ('TextField', 'TextField'),
    ('IntegerField', 'IntegerField'),
    ('FloatField', 'FloatField'),
    ('DecimalField', 'DecimalField'),
    ('BooleanField', 'BooleanField'),
    ('DateField', 'DateField'),
    ('DateTimeField', 'DateTimeField'),
]


