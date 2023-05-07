from django.apps import apps
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db import models
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

        # # Check if the model already exists
        # model = apps.get_model(
        #     app_label='productconfigurator', model_name=model_name)

        # If the model doesn't exist, create a new one
        if True:
            field_class = FIELD_TYPES.get(field_type, models.CharField)
            attrs = {
                field_name: field_class(max_length=50),
                '__module__': 'productconfigurator.models.validvaluetables',
            }
            model = type(model_name, (models.Model,), attrs)

        # Add the new field to the model
        model_class = apps.all_models['productconfigurator'][model_name]
        field = models.CharField(max_length=50)
        field.contribute_to_class(model_class, field_name)

        # Save the new model in the database
        model_obj = model(id=1)
        model_obj.save()

        # Save information about the new model in the DynamicModel table
        DynamicModel.objects.create(
            model_name=model_name, field_name=field_name, field_type=field_type)

        return HttpResponseRedirect(reverse('create_model'))
    else:
        return render(request, 'productconfigurator/create_model.html')
