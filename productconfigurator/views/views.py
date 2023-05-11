from django.db.models.base import ModelBase
from django.apps import apps
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db import models
from django.db import connection, migrations, models, transaction
from django.core.management import call_command
from django.db import DEFAULT_DB_ALIAS, connections


def productconfigurator(request):
    models = []
    for model in apps.get_app_config('productconfigurator').get_models():
        models.append(model.__name__)
    context = {'models': models, 'app_label': 'productconfigurator'}
    return render(request, 'productconfigurator/home.html', context)


DynamicModel = apps.get_model(
    app_label='productconfigurator', model_name='DynamicModel')


FIELD_TYPES = {
    'CharField': models.CharField,
    'IntegerField': models.IntegerField,
    'BooleanField': models.BooleanField,
    # add more field types as needed
}


def create_model(request):
    if request.method == 'POST':
        model_name = request.POST['model_name']
        field_name = request.POST['field_name']
        field_type = request.POST['field_type']

        # Check if the model already exists
        # model = apps.get_model(
        #     app_label='productconfigurator', model_name=model_name)

        # If the model doesn't exist, create a new one
        if True:
            field_class = FIELD_TYPES.get(field_type, models.CharField)
            attrs = {
                field_name: field_class(max_length=50),
                '__module__': 'productconfigurator.models.validvaluetables',
                '__init_subclass__': lambda cls: cls.add_to_class(field_name, field_class(max_length=50)),

            }
            model = ModelBase(model_name, (models.Model,), attrs)
            model._meta.app_label = 'productconfigurator'

            # Create a migration for the new model
            migration_name = f'0001_create_{model_name}_model'
            migration = type(migration_name, (migrations.Migration,), {
                'operations': [
                    migrations.CreateModel(
                        name=model_name,
                        fields=[(field_name, field_class(max_length=50))],
                        options={
                            'verbose_name': model_name,
                            'verbose_name_plural': model_name,
                        },
                    ),
                ],
                '__module__': 'productconfigurator.migrations',
            })
            print(migration_name)
            call_command('makemigrations', 'productconfigurator',
                         f'--name={migration_name}')

        # Run the migration to create the table
            with connection.cursor() as cursor:
                cursor.execute(
                    f"SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name = '{model_name}')")
                table_exists = cursor.fetchone()[0]
                if table_exists:
                    call_command('migrate', 'productconfigurator',
                                 f'--database={DEFAULT_DB_ALIAS}')
                else:
                    call_command('migrate', 'productconfigurator',
                                 f'{migration_name}', f'--database={DEFAULT_DB_ALIAS}')

            migration_name = f'0001_add_{field_name}_to_{model_name}'

        call_command('makemigrations', 'productconfigurator',
                     f'--name={migration_name}')

        # Run the migration to create the table
        with connection.cursor() as cursor:
            cursor.execute(
                f"SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name = '{model_name}')")
            table_exists = cursor.fetchone()[0]
            if table_exists:
                call_command('migrate', 'productconfigurator',
                             f'--database={DEFAULT_DB_ALIAS}')
            else:
                call_command('migrate', 'productconfigurator',
                             f'{migration_name}', f'--database={DEFAULT_DB_ALIAS}')
        # Save the new model in the database
        model_obj = model(id=1)
        model_obj.save()

        # Save information about the new model in the DynamicModel table
        DynamicModel.objects.create(
            model_name=model_name, field_name=field_name, field_type=field_type)

        return HttpResponseRedirect(reverse('create_model'))
    else:
        return render(request, 'productconfigurator/create_model.html')
