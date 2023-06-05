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
    ratebooks = apps.get_model('ratemanager', 'Ratebooks')
    allexhibits = apps.get_model('ratemanager', 'AllExhibits')
except LookupError:
    pass


class ViewRBForm(forms.ModelForm):

    class Meta:
        model = allexhibits
        fields = ()

    Carrier = forms.ModelChoiceField(
        queryset=carrier.objects.all().distinct(),
        label='Carrier'
    )

    StateCode = forms.ModelChoiceField(
        queryset=state.objects.all().distinct(),
        label='State Code'
    )

    UwCompany = forms.ModelChoiceField(
        queryset=uwCompany.objects.all().distinct(),
        label='UW Company Name'
    )

    LineOfBusiness = forms.ModelChoiceField(
        queryset=lineOfBusiness.objects.all().distinct(),
        label='Line of Business'
    )

    ProductName = forms.ModelChoiceField(
        queryset=productCode.objects.all().distinct(),
        label='Product Name'
    )

    RatebookGroup = forms.ModelChoiceField(
        queryset=rbGroups.objects.all().distinct(),
        label='Ratebook Group'
    )

    RatebookID = forms.ModelChoiceField(
        queryset=ratebooks.objects.all().distinct(),
        label='Ratebook ID'
    )

    RatebookVersion = forms.ModelChoiceField(
        queryset=ratebooks.objects.all().distinct(),
        label='Ratebook Version'
    )

    Exhibits = forms.ModelChoiceField(
        queryset=allexhibits.objects.all().distinct(),
        label='Exhibit Name'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
