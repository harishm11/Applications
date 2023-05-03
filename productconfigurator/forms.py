from django import forms
from django.apps import apps
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field
from django import forms

Productmodel = apps.get_model('productconfigurator', 'Productmodel')
Carriermodel = apps.get_model('productconfigurator', 'Carriermodel')


class ProductForm(forms.ModelForm):
    Carrier = forms.ModelChoiceField(queryset=Carriermodel.objects.all())

    class Meta:
        model = Productmodel
        fields = '__all__'
        widgets = {
            'EffectiveDate': forms.DateInput(attrs={'type': 'date'}),
            'ExpiryDate': forms.DateInput(attrs={'type': 'date'}),
            'OpenBookStartDate': forms.DateInput(attrs={'type': 'date'}),
            'CloseBookEndDate': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'

    def save(self, commit=True):
        instance = super(ProductForm, self).save(commit=False)
        if commit:
            instance.save()
        return instance
