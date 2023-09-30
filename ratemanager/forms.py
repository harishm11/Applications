from django import forms
from django.apps import apps
from datetime import datetime
from django.forms import inlineformset_factory
from ratemanager.models import RatebookMetadata, RatingFactors,\
    RatingExhibits, RatingVariables
from django.forms.models import BaseInlineFormSet
import ratemanager.views.HelperFunctions as helperfuncs
from django.utils.translation import gettext_lazy as _


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


class createTempleteForm(forms.ModelForm):

    CHOICES = [('new', 'New'),
               ('raterevision', 'Rate Revision'),
               ('refresh', 'Refresh/Update(Add/Remove Exhibits)'),
               ('factorcorrection', 'Factor Correction')]
    CreateIntent = forms.ChoiceField(
        label='Create Intent',
        choices=CHOICES,
        required=True,
        widget=forms.Select(),
        )

    class Meta:
        model = RatebookMetadata

        fields = (['Carrier', 'State', 'LineofBusiness',
                   'UWCompany', 'PolicyType', 'PolicySubType',
                   'ProductCode', 'ProjectID',
                   'NewBusinessEffectiveDate', 'RenewalEffectiveDate',
                   'MigrationDate', 'MigrationTime',
                   'ActivationDate', 'ActivationTime',
                   ])

        # exclude = (['RatebookName', 'RenewalExpiryDate', 'NewBusinessExpiryDate'])

        labels = dict()
        for i in fields:
            labels[i] = ' '.join(helperfuncs.camel_case_split(i))

        widgets = {
            'NewBusinessEffectiveDate': forms.widgets.DateInput(attrs={'type': 'date'}),
            'RenewalEffectiveDate': forms.widgets.DateInput(attrs={'type': 'date'}),
            'ActivationDate': forms.widgets.DateInput(attrs={'type': 'date'}),
            'ActivationTime': forms.widgets.TimeInput(attrs={'type': 'time', 'step': 'any'}),
            'MigrationDate': forms.widgets.DateInput(attrs={'type': 'date'}),
            'MigrationTime': forms.widgets.TimeInput(attrs={'type': 'time', 'step': 'any'})
        }


createRatingVariablesFromSet = inlineformset_factory(
    RatingExhibits,
    RatingVariables,
    fields=(['RatingVarName', 'RatingVarType', 'DisplayName']),
    extra=1,
    can_delete=True,
    max_num=15
    )


class BaseRatebookFormset(BaseInlineFormSet):

    def add_fields(self, form, index):
        super().add_fields(form, index)

        # Save the formset for a Exhibits RatingVars in the nested property.
        form.nested = createRatingVariablesFromSet(
            instance=form.instance,
            data=form.data if form.is_bound else None,
            files=form.files if form.is_bound else None,
            prefix="RatingVariables-%s-%s"
            % (form.prefix, createRatingVariablesFromSet.get_default_prefix())
        )

    def is_valid(self):
        """
        Also validate the nested formsets.
        """
        result = super().is_valid()

        if self.is_bound:
            for form in self.forms:
                if hasattr(form, "nested"):
                    result = result and form.nested.is_valid()

        return result

    def clean(self):
        """
        If a parent form has no data, but its nested forms do, we should
        return an error, because we can't save the parent.
        For example, if the Exhibit form is empty, but there are RatingVars.
        """
        super().clean()

        for form in self.forms:
            if not hasattr(form, "nested") or self._should_delete_form(form):
                continue

            if self._is_adding_nested_inlines_to_empty_form(form):
                form.add_error(
                    field=None,
                    error=_(
                        "You are trying to add variables to an exhibit which "
                        "does not yet exist. Please add information "
                        "about the exhibit and choose the variables again."
                    ),
                )

    def save(self, commit=True):
        """
        Also save the nested formsets.
        """
        result = super().save(commit=commit)

        for form in self.forms:
            if hasattr(form, "nested"):
                if not self._should_delete_form(form):
                    form.nested.save(commit=commit)

        return result

    def _is_adding_nested_inlines_to_empty_form(self, form):
        """
        Are we trying to add data in nested inlines to a form that has no data?
        e.g. Adding RatingVars to a new Exhibit whose data we haven't entered?
        """
        def is_empty_form(form):
            """
            A form is considered empty if it passes its validation,
            but doesn't have any data.

            This is primarily used in formsets, when you want to
            validate if an individual form is empty (extra_form).
            """
            if form.is_valid() and not form.cleaned_data:
                return True
            else:
                # Either the form has errors (isn't valid) or
                # it doesn't have errors and contains data.
                return False

        def is_form_persisted(form):
            """
            Does the form have a model instance attached and it's not being added?
            e.g. The form is about an existing Exhibit whose data is being edited.
            """
            if form.instance and not form.instance._state.adding:
                return True
            else:
                # Either the form has no instance attached or
                # it has an instance that is being added.
                return False
        if not hasattr(form, "nested"):
            # A basic form; it has no nested forms to check.
            return False

        if is_form_persisted(form):
            # We're editing (not adding) an existing model.
            return False

        if not is_empty_form(form):
            # The form has errors, or it contains valid data.
            return False

        # All the inline forms that aren't being deleted:
        non_deleted_forms = set(form.nested.forms).difference(
            set(form.nested.deleted_forms)
        )

        # At this point we know that the "form" is empty.
        # In all the inline forms that aren't being deleted, are there any that
        # contain data? Return True if so.
        return any(not is_empty_form(nested_form) for nested_form in non_deleted_forms)


createRatingExhibitsFromSet = inlineformset_factory(
    RatebookMetadata,
    RatingExhibits,
    fields=(['Exhibit', 'Coverages']),
    formset=BaseRatebookFormset,
    extra=1,
    can_delete=True,
    max_num=200,
    widgets={
        'Coverages': forms.CheckboxSelectMultiple()
    }
    )


class exportRBForm(forms.Form):
    CHOICES = [(None, None)]
    toExportExhibits = forms.MultipleChoiceField(
        choices=CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label='Select Exhibits to Export'
        )


class inputPKForm(forms.Form):
    pk = forms.IntegerField(label='Enter Ratebook Primary Key', required=True)
