from django import forms
from django.apps import apps

try:
    uwCompany = apps.get_model('systemtables', 'uwcompany')
    state = apps.get_model('systemtables', 'state')
    carrier = apps.get_model('systemtables', 'carrier')
    product = apps.get_model('productconfigurator', 'product')
    lineOfBusiness = apps.get_model('systemtables', 'lineofbusiness')
    productCode = apps.get_model('systemtables', 'productcode')
    policyType = apps.get_model('systemtables', 'policytype')
    policySubType = apps.get_model('systemtables', 'policysubtype')
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
        label='Carrier',
        required=False
    )

    StateCode = forms.ModelChoiceField(
        queryset=state.objects.all().distinct(),
        label='State Code',
        required=False
    )

    UwCompany = forms.ModelChoiceField(
        queryset=uwCompany.objects.all().distinct(),
        label='UW Company Name',
        required=False
    )

    LineOfBusiness = forms.ModelChoiceField(
        queryset=lineOfBusiness.objects.all().distinct(),
        label='Line of Business',
        required=False
    )

    PolicyType = forms.ModelChoiceField(
        queryset=policyType.objects.all().distinct(),
        label='Policy Type',
        required=False
    )

    PolicySubType = forms.ModelChoiceField(
        queryset=policySubType.objects.all().distinct(),
        label='Policy Sub Type',
        required=False
    )

    ProductName = forms.ModelChoiceField(
        queryset=productCode.objects.all().filter().values_list('ProductName', flat=True).order_by('ProductName').distinct(),
        label='Product Name',
        required=False
    )

    RatebookGroup = forms.ModelChoiceField(
        queryset=rbGroups.objects.all().distinct(),
        label='Ratebook Group',
        required=False,
        widget=forms.Select(attrs={'onchange': 'this.form.submit();'})
    )

    RatebookVersion = forms.ModelChoiceField(
        queryset=ratebooks.objects.filter().values_list('RatebookVersion', flat=True).order_by('RatebookVersion').distinct(),
        label='Ratebook Version',
        required=False
    )

    RatebookRevisionType = forms.ModelChoiceField(
        queryset=ratebooks.objects.filter().values_list('RatebookRevisionType', flat=True).order_by('RatebookRevisionType').distinct(),
        label='Ratebook Revision Type',
        required=False
    )

    RatebookStatusType = forms.ModelChoiceField(
        queryset=ratebooks.objects.filter().values_list('RatebookStatusType', flat=True).order_by('RatebookStatusType').distinct(),
        label='Ratebook Status Type',
        required=False
    )

    RatebookChangeType = forms.ModelChoiceField(
        queryset=ratebooks.objects.filter().values_list('RatebookChangeType', flat=True).order_by('RatebookChangeType').distinct(),
        label='Ratebook Change Type',
        required=False
    )

    RatebookID = forms.ModelChoiceField(
        queryset=ratebooks.objects.all().distinct(),
        label='Ratebook ID',
        required=False
    )

    Exhibit = forms.ModelChoiceField(
        queryset=allexhibits.objects.filter().values_list('Exhibit', flat=True).order_by('Exhibit').distinct(),
        label='Exhibit Name',
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
