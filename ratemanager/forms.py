from django import forms
from django.apps import apps
from datetime import datetime
from ratemanager.models import comments

from ratemanager.models.ratebookmetadata import RatebookMetadata
from ratemanager.models.ratebooktemplate import RatebookTemplate
from ratemanager.models.ratingfactors import RatingFactors
from ratemanager.models.ratingexhibits import RatingExhibits

from django.contrib.admin.widgets import FilteredSelectMultiple


try:
    uwCompany = apps.get_model('systemtables', 'uwcompany')
    state = apps.get_model('systemtables', 'state')
    carrier = apps.get_model('systemtables', 'carrier')
    product = apps.get_model('productconfigurator', 'product')
    lineOfBusiness = apps.get_model('systemtables', 'lineofbusiness')
    productCode = apps.get_model('systemtables', 'productcode')
    policyType = apps.get_model('systemtables', 'policytype')
    policySubType = apps.get_model('systemtables', 'policysubtype')
except LookupError:
    pass


def setVerboseNamesAsLabels(self):
    self.fields['LineofBusiness'].label = lineOfBusiness._meta.get_field(
        'LobName').verbose_name
    self.fields['State'].label = state._meta.get_field(
        'StateCode').verbose_name
    self.fields['Carrier'].label = carrier._meta.get_field(
        'CarrierName').verbose_name
    self.fields['UWCompany'].label = uwCompany._meta.get_field(
        'CompanyName').verbose_name
    self.fields['ProductCode'].label = productCode._meta.get_field(
        'ProductCd').verbose_name
    self.fields['PolicyType'].label = policyType._meta.get_field(
        'PolicyTypeName').verbose_name
    self.fields['PolicySubType'].label = policySubType._meta.get_field(
        'PolicySubTypeName').verbose_name


class ViewRBForm(forms.ModelForm):

    class Meta:
        model = RatebookMetadata
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
        model = RatingFactors
        fields = ()

    TableCategory = forms.ModelChoiceField(
        queryset=RatingFactors.objects.filter().values_list('TableCategory', flat=True).distinct(),
        label='Table Category',
        required=False,
        widget=forms.Select(attrs={'onchange': 'this.form.submit();'})
    )

    Exhibit = forms.ModelChoiceField(
        queryset=RatingFactors.objects.filter().values_list('Exhibit', flat=True).order_by('Exhibit').distinct(),
        label='Exhibit Name',
        required=False,
        widget=forms.Select(attrs={'onchange': 'this.form.submit();'})
    )

    PivotView = forms.ChoiceField(
        choices=(
            ('on', 'Spreadsheet Table View'),
            ('off', 'Internal Table View')
            ),
        label='',
        required=True,
        initial='on',
        widget=forms.Select(attrs={'id': 'RatebookUpdateType',
                                   'onchange': 'this.form.submit();'})
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.initial.get('TableCategory') != '':
            self.fields['Exhibit'].queryset = RatingFactors.objects.\
                filter(TableCategory=self.initial.get('TableCategory'),
                       RatebookID=self.initial.get('RatebookID')).\
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


class SelectExhibitFormWithDate(SelectExhibitForm):
    class Meta:
        model = RatingFactors
        fields = ()

    QueryDate = forms.DateField(
        label='Query Date',
        initial=datetime.today(),
        widget=forms.widgets.DateInput(
            attrs={
                'type': 'date',
                'onchange': 'this.form.submit();'
                }
        )
    )


class ViewRBFormWithDate(ViewRBForm):

    NewBusinessEffectiveDate = forms.DateField(
        label='New Business Effective Date',
        initial=datetime.today(),
        widget=forms.widgets.DateInput(
            attrs={
                'type': 'date',
                'onchange': 'this.form.submit();'
                }
        )
    )

    RenewalEffectiveDate = forms.DateField(
        label='Renewal Effective Date',
        initial=datetime.today(),
        widget=forms.widgets.DateInput(
            attrs={
                'type': 'date',
                'onchange': 'this.form.submit();'
                }
        )
    )

    ActivationDate = forms.DateField(
        label='Activation Date',
        initial=datetime.today(),
        widget=forms.widgets.DateInput(
            attrs={
                'type': 'date',
                'onchange': 'this.form.submit();'
                }
        )
    )

    MigrationDate = forms.DateField(
        label='Migration Date',
        initial=datetime.today(),
        widget=forms.widgets.DateInput(
            attrs={
                'type': 'date',
                'onchange': 'this.form.submit();'
                }
        )
    )

    CreationDateTime = forms.DateField(
        label='Creation/Upload Date',
        initial=datetime.today(),
        widget=forms.widgets.DateInput(
            attrs={
                'type': 'date',
                'onchange': 'this.form.submit();'
                }
        )
    )


class createTemplateForm(forms.ModelForm):
    class Meta:
        model = RatebookMetadata

        fields = ([
            'State', 'Carrier', 'LineofBusiness',
            'UWCompany', 'PolicyType', 'PolicySubType',
            'ProductCode'
        ])

        # exclude = ([])

        labels = dict()
        for i in fields:
            # appModel = apps.get_model('systemtables', i.lower().replace(' ', ''))
            labels[i] = RatebookMetadata._meta.get_field(i).verbose_name

        widgets = {
            'State': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'Carrier': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'LineofBusiness': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'UWCompany': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'PolicyType': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'PolicySubType': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'ProductCode': forms.Select(attrs={'class': 'form-control form-control-sm'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        setVerboseNamesAsLabels(self)


class projectIdAndDateInputForm(forms.ModelForm):
    class Meta:
        model = RatebookMetadata

        fields = ([
                    'NewBusinessEffectiveDate', 'RenewalEffectiveDate',
                    'ProjectDescription', 'RatebookChangeType'
                    ])

        # exclude = (['RatebookName', 'RenewalExpiryDate', 'NewBusinessExpiryDate','MigrationDate', 'MigrationTime', 'ActivationDate', 'ActivationTime', 'ProjectID',])

        labels = dict()
        for i in fields:
            labels[i] = RatebookMetadata._meta.get_field(i).verbose_name

        widgets = {
            'NewBusinessEffectiveDate': forms.widgets.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'}),
            'RenewalEffectiveDate': forms.widgets.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'}),
            'ActivationDate': forms.widgets.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'}),
            'ActivationTime': forms.widgets.TimeInput(attrs={'type': 'time', 'step': 'any', 'class': 'form-control form-control-sm'}),
            'MigrationDate': forms.widgets.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'}),
            'MigrationTime': forms.widgets.TimeInput(attrs={'type': 'time', 'step': 'any', 'class': 'form-control form-control-sm'}),
            'ProjectDescription': forms.Textarea(attrs={"rows": "2", 'class': 'form-control form-control-sm'}),
            'ProjectID': forms.Textarea(attrs={"rows": "1", 'class': 'form-control form-control-sm'}),
            'RatebookChangeType': forms.Select(attrs={'class': 'form-control form-control-sm'}),
        }


class exportRBForm(forms.Form):
    CHOICES = [(None, None)]
    toExportExhibits = forms.MultipleChoiceField(
        choices=CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label='Select Exhibits to Export'
        )


class editExhibitForm(forms.ModelForm):
    class Meta:
        # fields from RatebookTemplate model
        model = RatebookTemplate
        fields = ([
            'RatebookExhibit', 'ExhibitVariables', 'ExhibitCoverages'
        ])

        widgets = {'ExhibitVariables': forms.CheckboxSelectMultiple(),
                   'ExhibitCoverages': forms.CheckboxSelectMultiple()}
        labels = dict()
        for i in fields:
            labels[i] = ' '.join(i)
        labels['RatebookExhibit'] = 'Exhibit Name'


class addExhibitForm(forms.ModelForm):
    class Meta:
        # fields from RatebookTemplate model
        model = RatingExhibits
        fields = (['Exhibit', 'DisplayName'])
        labels = {
            'Exhibit': 'Exhibit Name'
        }
        # labels = dict()
        # for i in fields:
        #     labels[i] = ' '.join(helperfuncs.camel_case_split(i))


class selectExhibitListsForm(forms.ModelForm):
    toAddExhibits = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=FilteredSelectMultiple("Exhibits", False),
        label='Select Exhibits to Add to the Template',
        required=False
        )

    class Media:
        css = {
            'all': ['admin/css/widgets.css',
                    'css/FilteredSelectMultiple.css'],
        }
        # Adding this javascript is crucial
        js = ['/admin/jsi18n/']

    class Meta:
        model = RatebookTemplate
        fields = ()


class selectExhibitListsFormExistingRB(selectExhibitListsForm):
    def __init__(self, *args, **kwargs):
        rbID = kwargs.pop('rbID')
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        choices = RatebookTemplate.objects.all().filter(RatebookID=rbID)
        self.fields['toAddExhibits'].queryset = RatingExhibits.objects.filter(ratebooktemplate__in=choices)


class searchCriteriaForm(createTemplateForm):
    pass


class ratesUploadForm(forms.Form):
    file = forms.FileField(
        label="Select the Excel file to upload:",
        help_text="Download the template Excel file from the Ratebook tab and upload it with the rates filled-in.",
        widget=forms.FileInput(attrs={'class': 'form-control form-control-sm'})
    )


class ratesReviewForm(forms.ModelForm):
    class Meta:
        model = comments.Notes
        fields = ('Note',)
        widgets = {'Note': forms.Textarea(
            attrs={
                "rows": "3",
                'class': 'form-control form-control-sm'}),
                }
