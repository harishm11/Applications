import os
from django import forms
from django.apps import apps
from django.db import models
from django.core.management import call_command
state = apps.get_model('productconfigurator', 'state')
carrier = apps.get_model('productconfigurator', 'carrier')
product = apps.get_model('productconfigurator', 'product')
try:
    uwcompany = apps.get_model('productconfigurator', 'uwcompany')
except LookupError:
    uwcompany = None


class ProductForm(forms.ModelForm):

    Carrier = forms.ModelChoiceField(
        queryset=carrier.objects.all(),
        label='Carrier'
    )
    StateCode = forms.ModelChoiceField(
        queryset=state.objects.all(),
        label='StateCode'
    )

    # CompanyName = forms.ModelChoiceField(
    #     queryset=uwcompany.objects.all(),
    #     label='CompanyName'
    # )

    class Meta:
        model = product
        fields = '__all__'
        widgets = {
            'OpenBookStartDate': forms.DateInput(attrs={'type': 'date'}),
            'CloseBookEndDate': forms.DateInput(attrs={'type': 'date'}),
            'EffectiveDate': forms.DateInput(attrs={'type': 'date'}),
            'ExpiryDate': forms.DateInput(attrs={'type': 'date'}),
        }


FIELD_TYPE_CHOICES = (
    ('CharField', 'CharField'),
    ('IntegerField', 'IntegerField'),
    ('DateField', 'DateField'),
    ('DateTimeField', 'DateTimeField'),
    ('EmailField', 'EmailField'),
)


class CreateModelForm(forms.Form):
    model_name = forms.CharField(max_length=100)
    field_names = forms.CharField(widget=forms.Textarea)
    field_types = forms.MultipleChoiceField(choices=FIELD_TYPE_CHOICES)

    def save_model(self):
        model_name = self.cleaned_data['model_name']
        field_names = self.cleaned_data['field_names'].split('\n')
        field_types = self.cleaned_data['field_types']
        model = self.create_model(model_name, field_names, field_types)
        self.generate_migration(model)
        self.apply_migrations(model)

    def create_model(self, model_name, field_names, field_types):
        fields = {}
        model_code = f"from django.db import models\n"
        model_code += f"class {model_name}(models.Model):\n"
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

        # meta_attrs = {'db_table': model_name.lower()}

        class Meta:
            # db_table = meta_attrs['db_table']
            app_label = 'productconfigurator'
        attrs = {
            '__module__': 'models',
            '__name__': model_name,
            'Meta': Meta,
        }
        attrs.update(fields)
        model = type(model_name, (models.Model,), dict(attrs))
        filename = f"{model_name.lower()}.py"
        filepath = os.path.join("Configuration/productconfigurator",
                                "models/validvaluetables", filename)

        if not os.path.exists(filepath):
            with open(filepath, "w") as f:
                f.write(model_code)
        apps.all_models['productconfigurator'][model_name] = model

        return model

    def get_previous_migration(self, app_label):
        migration_dir = f"COnfiguration/{app_label}/migrations"
        migration_files = os.listdir(migration_dir)
        migration_files = filter(lambda f: f.endswith('.py'), migration_files)
        migration_files = sorted(migration_files)

        if len(migration_files) > 1:
            return f"{migration_files[-2].split('.py')[0]}"
        else:
            return None

    def generate_migration(self, model):
        app_label = model._meta.app_label
        call_command('makemigrations', app_label)

    def apply_migrations(self, model):
        # app_label = model._meta.app_label
        # previous_migration = self.get_previous_migration(app_label)
        # if previous_migration:
        #     dependencies = [(f"{app_label}", f"{previous_migration}")]
        # else:
        #     dependencies = []
        call_command('migrate', model._meta.app_label)
