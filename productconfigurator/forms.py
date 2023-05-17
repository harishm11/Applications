
from django import forms
from django.apps import apps
from django.core.management import call_command


try:
    uwcompany = apps.get_model('systemtables', 'uwcompany')
    state = apps.get_model('systemtables', 'state')
    carrier = apps.get_model('systemtables', 'carrier')
    product = apps.get_model('productconfigurator', 'product')
    lineofbusiness = apps.get_model('systemtables', 'lineofbusiness')
    policytype = apps.get_model('systemtables', 'policytype')
    policysubtype = apps.get_model('systemtables', 'policysubtype')
    offering = apps.get_model('systemtables', 'offering')
    productcode = apps.get_model('systemtables', 'productcode')
    policyterm = apps.get_model('systemtables', 'policyterm')

except LookupError:
    None


class ProductForm(forms.ModelForm):

    Carrier = forms.ModelChoiceField(
        queryset=carrier.objects.all(),
        label='Carrier'
    )
    StateCode = forms.ModelChoiceField(
        queryset=state.objects.all(),
        label='StateCode'
    )

    UwCompany = forms.ModelChoiceField(
        queryset=uwcompany.objects.all(),
        label='CompanyName'
    )

    LineOfBusiness = forms.ModelChoiceField(
        queryset=lineofbusiness.objects.all(),
        label='LobName'
    )

    PolicyType = forms.ModelChoiceField(
        queryset=policytype.objects.all(),
        label='PolicyType',
        widget=forms.Select(attrs={'onchange': 'this.form.submit();'})
    )

    ProductCode = forms.ModelChoiceField(
        queryset=productcode.objects.all(),
        label='ProductCode'
    )

    PolicySubType = forms.ModelChoiceField(
        queryset=policysubtype.objects.all(),
        label='PolicySubType'
    )
    Offering = forms.ModelChoiceField(
        queryset=offering.objects.all(),
        label='OfferingName'
    )
    Policyterm = forms.ModelChoiceField(
        queryset=policyterm.objects.all(),
        label='Policyterm'
    )

    class Meta:
        model = product
        exclude = ['coverages', 'discounts', 'surcharges']
        widgets = {
            'OpenBookStartDate': forms.DateInput(attrs={'type': 'date'}),
            'CloseBookEndDate': forms.DateInput(attrs={'type': 'date'}),
            'EffectiveDate': forms.DateInput(attrs={'type': 'date'}),
            'ExpiryDate': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'PolicyType' in self.data:
            policytype_id = int(self.data.get('PolicyType'))
            self.fields['PolicySubType'].queryset = policysubtype.objects.filter(
                PolicyType_id=policytype_id)
        elif self.instance.pk:
            self.fields['PolicySubType'].queryset = self.instance.PolicyType.policysubtype_set.all()


class PolicySubTypeForm(forms.ModelForm):
    PolicyType = forms.ModelChoiceField(queryset=policytype.objects.all())

    class Meta:
        model = policysubtype
        fields = '__all__'
