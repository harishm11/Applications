from django import forms
from django.apps import apps
from crispy_forms.helper import FormHelper
from django import forms
# from django.forms import inlineformset_factory
Product = apps.get_model(
    'productconfigurator', 'Product')
coverage = apps.get_model(
    'productconfigurator', 'coverage')


class CoverageForm(forms.ModelForm):
    CoverageSequence = forms.IntegerField(
        widget=forms.NumberInput(attrs={'type': 'number'}))

    class Meta:
        model = coverage
        fields = '__all__'
        widgets = {
            'Product': forms.NumberInput(attrs={'type': 'number'}),
            'EffectiveDate': forms.DateInput(attrs={'type': 'date'}),
            'ExpiryDate': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super(CoverageForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'

    def save(self, commit=True):
        instance = super(CoverageForm, self).save(commit=False)
        if commit:
            instance.save()
        return instance
