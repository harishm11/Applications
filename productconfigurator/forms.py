
from django import forms
from django.apps import apps
from django.core.management import call_command
from django.shortcuts import render,  redirect
from django.core.exceptions import ValidationError

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
    coverage = apps.get_model('systemtables', 'coverage')

except LookupError:
    None


class ProductForm(forms.ModelForm):

    LineOfBusiness = forms.ModelChoiceField(
        queryset=lineofbusiness.objects.all(),
        label='LineOfBusiness',
        widget=forms.Select(attrs={'onchange': 'this.form.submit();'})
    )

    PolicyType = forms.ModelChoiceField(
        queryset=policytype.objects.all(),
        label='PolicyType',
        widget=forms.Select(attrs={'onchange': 'this.form.submit();'})
    )

    ProductCode = forms.ModelChoiceField(
        queryset=productcode.objects.all(),
        label='ProductCode',
        widget=forms.Select(attrs={'onchange': 'this.form.submit();'})
    )

    OpenBookStartDate = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    CloseBookEndDate = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    EffectiveDate = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date'}), required=True)
    ExpiryDate = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date'}), required=False)

    class Meta:
        model = product

        exclude = ('coverages', 'discounts', 'surcharges',)

    # def combination_exists(self):
    #     cleaned_data = super().clean()
    #     state_code = cleaned_data.get('StateCode')
    #     carrier = cleaned_data.get('Carrier')
    #     uw_company = cleaned_data.get('UwCompany')
    #     line_of_business = cleaned_data.get('LineOfBusiness')
    #     policy_type = cleaned_data.get('PolicyType')
    #     policy_sub_type = cleaned_data.get('PolicySubType')
    #     policy_term = cleaned_data.get('Policyterm')
    #     product_code = cleaned_data.get('ProductCode')
    #     # Check if the combination already exists
    #     if product.objects.filter(StateCode=state_code, Carrier=carrier, UwCompany=uw_company,
    #                               LineOfBusiness=line_of_business, PolicyType=policy_type,
    #                               PolicySubType=policy_sub_type, Policyterm=policy_term, ProductCode=product_code).exists():
    #         return 'Product already exists. Please enter a unique Product.'

    #     return ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        policy_type_id = self.data.get('PolicyType') or getattr(
            self.instance, 'PolicyType_id', None)
        if policy_type_id is not None:
            try:
                policy_type_id = int(policy_type_id)
            except ValueError:
                policy_type_id = None
        self.fields['PolicySubType'].queryset = policysubtype.objects.filter(
            PolicyType_id=policy_type_id) if policy_type_id else policysubtype.objects.none()

        lob_id = self.data.get('LineOfBusiness') or getattr(
            self.instance, 'LineOfBusiness_id', None)
        if lob_id is not None:
            try:
                lob_id = int(lob_id)
            except ValueError:
                lob_id = None
        self.fields['ProductCode'].queryset = productcode.objects.filter(
            Lob_id=lob_id) if lob_id else productcode.objects.none()
        self.fields['Policyterm'].queryset = policyterm.objects.filter(
            Lob_id=lob_id) if lob_id else policyterm.objects.none()
        self.fields['PolicyType'].queryset = policytype.objects.filter(
            Lob_id=lob_id) if lob_id else policytype.objects.none()


class PolicySubTypeForm(forms.ModelForm):
    PolicyType = forms.ModelChoiceField(queryset=policytype.objects.all())

    class Meta:
        model = policysubtype
        fields = '__all__'


class ProductFilterForm(forms.Form):
    Carrier = forms.ModelChoiceField(
        queryset=carrier.objects.all(),
        required=False,
        label='Carrier',
        widget=forms.Select(attrs={'onchange': 'this.form.submit();'})
    )
    StateCode = forms.ModelChoiceField(
        queryset=state.objects.all(),
        required=False,
        label='StateCode',
        widget=forms.Select(attrs={'onchange': 'this.form.submit();'})
    )

    # UwCompany = forms.ModelChoiceField(
    #     queryset=uwcompany.objects.all(),
    #     required=False,
    #     label='CompanyName'
    # )

    LineOfBusiness = forms.ModelChoiceField(
        queryset=lineofbusiness.objects.all(),
        required=False,
        label='LobName',
        widget=forms.Select(attrs={'onchange': 'this.form.submit();'})
    )

    PolicyType = forms.ModelChoiceField(
        queryset=policytype.objects.all(),
        required=False,
        label='PolicyType',
        widget=forms.Select(attrs={'onchange': 'this.form.submit();'})
    )

    PolicySubType = forms.ModelChoiceField(
        queryset=policysubtype.objects.none(),
        required=False,
        label='PolicySubType',
        widget=forms.Select(attrs={'onchange': 'this.form.submit();'})
    )

    ProductCode = forms.ModelChoiceField(
        queryset=productcode.objects.all(),
        required=False,
        label='ProductCode',
        widget=forms.Select(attrs={'onchange': 'this.form.submit();'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        policy_type_id = self.data.get('PolicyType')
        if policy_type_id is not None:
            try:
                policy_type_id = int(policy_type_id)
            except ValueError:
                policy_type_id = None
        self.fields['PolicySubType'].queryset = policysubtype.objects.filter(
            PolicyType_id=policy_type_id) if policy_type_id else policysubtype.objects.none()

        lob_id = self.data.get('LineOfBusiness')
        if lob_id is not None:
            try:
                lob_id = int(lob_id)
            except ValueError:
                lob_id = None
        self.fields['ProductCode'].queryset = productcode.objects.filter(
            Lob_id=lob_id) if lob_id else productcode.objects.none()
        self.fields['PolicyType'].queryset = policytype.objects.filter(
            Lob_id=lob_id) if lob_id else policytype.objects.none()
