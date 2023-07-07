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
    ratebooks = apps.get_model('ratemanager', 'Ratebooks')
    allexhibits = apps.get_model('ratemanager', 'AllExhibits')
except LookupError:
    pass


class ViewRBForm(forms.ModelForm):

    class Meta:
        model = ratebooks
        fields = ()

    StateCode = forms.ModelChoiceField(
        queryset=state.objects.all().distinct().order_by('id'),
        label='State Code',
        required=False,
        widget=forms.Select(attrs={'onchange': 'this.form.submit();'})
    )

    Carrier = forms.ModelChoiceField(
        queryset=carrier.objects.all().distinct().order_by('CarrierName'),
        label='Carrier',
        required=False,
        widget=forms.Select(attrs={'onchange': 'this.form.submit();'})
    )

    UWCompany = forms.ModelChoiceField(
        queryset=uwCompany.objects.all().distinct().order_by('CompanyName'),
        label='UW Company Name',
        required=False,
        widget=forms.Select(attrs={'onchange': 'this.form.submit();'})
    )

    LineofBusiness = forms.ModelChoiceField(
        queryset=lineOfBusiness.objects.all().distinct(),
        label='Line of Business',
        required=False,
        widget=forms.Select(attrs={'onchange': 'this.form.submit();'})
    )

    PolicyType = forms.ModelChoiceField(
        queryset=policyType.objects.all().distinct(),
        label='Policy Type',
        required=False,
        widget=forms.Select(attrs={'onchange': 'this.form.submit();'})
    )

    PolicySubType = forms.ModelChoiceField(
        queryset=policySubType.objects.all().distinct(),
        label='Policy Sub Type',
        required=False,
        widget=forms.Select(attrs={'onchange': 'this.form.submit();'})
    )

    ProductCode = forms.ModelChoiceField(
        queryset=productCode.objects.all().distinct(),
        label='Product Code',
        required=False,
        widget=forms.Select(attrs={'onchange': 'this.form.submit();'})
    )


class SelectExhibitForm(forms.ModelForm):
    class Meta:
        model = allexhibits
        fields = ()

    TableCategory = forms.ModelChoiceField(
        queryset=allexhibits.objects.filter().values_list('TableCategory', flat=True).distinct(),
        label='Table Category',
        required=False,
        widget=forms.Select(attrs={'onchange': 'this.form.submit();'})
    )

    Exhibit = forms.ModelChoiceField(
        queryset=allexhibits.objects.filter().values_list('Exhibit', flat=True).order_by('Exhibit').distinct(),
        label='Exhibit Name',
        required=False,
        widget=forms.Select(attrs={'onchange': 'this.form.submit();'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.initial.get('TableCategory') != '':
            self.fields['Exhibit'].queryset = allexhibits.objects.\
                filter(TableCategory=self.initial.get('TableCategory'),
                       Ratebook=self.initial.get('Ratebook')).\
                values_list('Exhibit', flat=True).order_by('Exhibit').distinct()


class UpdateForm(forms.Form):
    RatebookUpdateType = forms.ChoiceField(
        label='Is it a minor update or major update?',
        choices=(
            ('minor', 'Minor'),
            ('major', 'Major')
            ),
        required=True,
        widget=forms.Select(attrs={'id': 'RatebookUpdateType'})
        )
