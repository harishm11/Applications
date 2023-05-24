from django import forms
from django.apps import apps

try:
    uwCompany = apps.get_model('systemtables', 'uwcompany')
    state = apps.get_model('systemtables', 'state')
    carrier = apps.get_model('systemtables', 'carrier')
    product = apps.get_model('productconfigurator', 'product')
    lineOfBusiness = apps.get_model('systemtables', 'lineofbusiness')
    productCode = apps.get_model('systemtables', 'productcode')
    rbGroups = apps.get_model('ratemanager', 'RatebookGroups')
except LookupError:
    pass


class ViewRBForm(forms.ModelForm):

    class Meta:
        model = rbGroups
        fields = ()

    Carrier = forms.ModelChoiceField(
        queryset=carrier.objects.all(),
        label='Carrier'
    )

    StateCode = forms.ModelChoiceField(
        queryset=state.objects.all(),
        label='State Code'
    )

    UwCompany = forms.ModelChoiceField(
        queryset=uwCompany.objects.all(),
        label='UW Company Name'
    )

    LineOfBusiness = forms.ModelChoiceField(
        queryset=lineOfBusiness.objects.all(),
        label='Line of Business'
    )

    ProductName = forms.ModelChoiceField(
        queryset=productCode.objects.all(),
        label='Product Name'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
