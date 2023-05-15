import os
from django import forms
from django.apps import apps
from django.db import models
from django.core.management import call_command


try:
    uwcompany = apps.get_model('productconfigurator', 'uwcompany')
    state = apps.get_model('productconfigurator', 'state')
    carrier = apps.get_model('productconfigurator', 'carrier')
    product = apps.get_model('productconfigurator', 'product')
    lineofbusiness = apps.get_model('productconfigurator', 'lineofbusiness')
    policytype = apps.get_model('productconfigurator', 'policytype')
    policysubtype = apps.get_model('productconfigurator', 'policysubtype')
    offering = apps.get_model('productconfigurator', 'offering')
    productcode = apps.get_model('productconfigurator', 'productcode')
    policyterm = apps.get_model('productconfigurator', 'policyterm')

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
        queryset=policyterm.objects.none(),
        label='Policyterm'
    )

    class Meta:
        model = product
        fields = '__all__'
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


FIELD_TYPE_CHOICES = (
    ('CharField', 'CharField'),
    ('IntegerField', 'IntegerField'),
    ('DateField', 'DateField'),
    ('DateTimeField', 'DateTimeField'),
    ('EmailField', 'EmailField'),
)


class CreateModelForm(forms.Form):
    modelName = forms.CharField(max_length=100)
    field_names = forms.CharField(widget=forms.Textarea)
    field_types = forms.MultipleChoiceField(choices=FIELD_TYPE_CHOICES)

    def saveModel(self):
        modelName = self.cleaned_data['modelName']
        field_names = self.cleaned_data['field_names'].split('\n')
        field_types = self.cleaned_data['field_types']
        model = self.createModel(modelName, field_names, field_types)
        self.generate_migration(model)
        self.apply_migrations(model)

    def createModel(self, modelName, field_names, field_types):
        fields = {}
        model_code = f"from django.db import models\n"
        model_code += f"class {modelName}(models.Model):\n"
        for name, field_type in zip(field_names, field_types):
            field_args = ""
            if field_type == "CharField":
                fields[name] = models.CharField(
                    max_length=255, null=True, blank=True)
                field_args = "max_length=255,null=True,blank=True"
            elif field_type == "IntegerField":
                field_args = "default=0"
                fields[name] = models.IntegerField(default=0)
            elif field_type == "DateField":
                field_args = "auto_now_add=True"
                fields[name] = models.DateField(auto_now_add=True)
            elif field_type == "DateTimeField":
                field_args = "auto_now_add=True"
                fields[name] = models.DateTimeField(auto_now_add=True)
            elif field_type == "EmailField":
                field_args = "max_length=255"
                fields[name] = models.IntegerField(max_length=255)

            model_code += f"    {name} = models.{field_type}({field_args})\n"

        # meta_attrs = {'db_table': modelName.lower()}
        model_code += f"   def __str__(self):\n"
        model_code += f"  return self.{name}"

        class Meta:
            # db_table = meta_attrs['db_table']
            app_label = 'productconfigurator'
        attrs = {
            '__module__': 'models',
            '__name__': modelName,
            'Meta': Meta,
        }
        attrs.update(fields)
        model = type(modelName, (models.Model,), dict(attrs))
        filename = f"{modelName.lower()}.py"
        filepath = os.path.join("Configuration/productconfigurator",
                                "models", filename)
        print(filepath)
        if not os.path.exists(filepath):
            with open(filepath, "w") as f:
                f.write(model_code)
        apps.all_models['productconfigurator'][modelName] = model

        return model

    def get_previous_migration(self, appLabel):
        migration_dir = f"COnfiguration/{appLabel}/migrations"
        migration_files = os.listdir(migration_dir)
        migration_files = filter(lambda f: f.endswith('.py'), migration_files)
        migration_files = sorted(migration_files)

        if len(migration_files) > 1:
            return f"{migration_files[-2].split('.py')[0]}"
        else:
            return None

    def generate_migration(self, model):
        appLabel = model._meta.app_label
        call_command('makemigrations', appLabel)

    def apply_migrations(self, model):
        # appLabel = model._meta.appLabel
        # previous_migration = self.get_previous_migration(appLabel)
        # if previous_migration:
        #     dependencies = [(f"{appLabel}", f"{previous_migration}")]
        # else:
        #     dependencies = []
        call_command('migrate', model._meta.app_label)
