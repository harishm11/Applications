import csv
from django.http import HttpResponse
from django.forms.models import modelform_factory
from django.apps import apps
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.forms import modelform_factory
from django import forms
from productconfigurator.forms import *


def getModelNames(appLabel):
    options = []
    for model in apps.get_app_config(appLabel).get_models():
        options.append(model.__name__)

    modelnames = {'options': options}
    return modelnames


def datatable(request, appLabel, modelName):
    try:
        Model = apps.get_model(appLabel, modelName)
        model_fields = [field.name for field in Model._meta.fields]

        verboseNamePlural = Model._meta.verbose_name_plural
        search_query = request.GET.get('search', '')
        if search_query:
            q_objects = Q()
            for field in model_fields:
                q_objects |= Q(**{f'{field}__icontains': search_query})
            objects = Model.objects.filter(q_objects)
        else:
            objects = Model.objects.all()

        context = {
            'Model': Model,
            'model_fields': model_fields,
            'objects': objects,
            'verboseNamePlural_value': verboseNamePlural,
            'appLabel': appLabel,
            'modelName': modelName,
            'search_query': search_query,


        }
        context.update(getModelNames(appLabel))

        return render(request, 'datatable/datatable.html', context)
    except Exception as err:
        return render(request, 'error.html', {'message': err})


def addObject(request, appLabel, modelName):
    try:
        Model = apps.get_model(appLabel, modelName)
        if modelName == 'Product':
            form_obj = ProductForm(request.POST)
        else:
            form_obj = modelform_factory(Model, exclude=('id',), widgets={
                'OpenBookStartDate': forms.DateInput(attrs={'type': 'date'}),
                'CloseBookEndDate': forms.DateInput(attrs={'type': 'date'}),
                'EffectiveDate': forms.DateInput(attrs={'type': 'date'}),
                'ExpiryDate': forms.DateInput(attrs={'type': 'date'}),
            })
        verboseNamePlural = Model._meta.verbose_name_plural
        if request.method == 'POST':
            if modelName != 'Product':
                form = form_obj(request.POST)
            else:
                form = form_obj
            if form.is_valid():
                form.save()
                return redirect('datatable', appLabel=appLabel, modelName=modelName)
        else:
            form = form_obj

        context = {
            'form': form,
            'appLabel': appLabel,
            'modelName': modelName,
            'verboseNamePlural_value': verboseNamePlural,
        }
        context.update(getModelNames(appLabel))

        return render(request, 'datatable/add.html', context)
    except Exception as err:
        return render(request, 'error.html', {'message': err})


def editObject(request, appLabel, modelName, object_id):
    try:
        Model = apps.get_model(appLabel, modelName)
        instance = get_object_or_404(Model, pk=object_id)

        form = modelform_factory(Model, exclude=('id',), widgets={
            'OpenBookStartDate': forms.DateInput(attrs={'type': 'date'}),
            'CloseBookEndDate': forms.DateInput(attrs={'type': 'date'}),
            'EffectiveDate': forms.DateInput(attrs={'type': 'date'}),
            'ExpiryDate': forms.DateInput(attrs={'type': 'date'}),

        })

        verboseNamePlural = Model._meta.verbose_name_plural
        if request.method == 'POST':
            form = form(request.POST, instance=instance)
            if form.is_valid():
                form.save()
                return redirect('datatable', appLabel=appLabel, modelName=modelName)

        context = {
            'form': form(instance=instance),
            'appLabel': appLabel,
            'modelName': modelName,
            'object_id': object_id,
            'verboseNamePlural_value': verboseNamePlural,
        }

        return render(request, 'datatable/edit.html', context)
    except Exception as err:
        return render(request, 'error.html', {'message': err})


def deleteObject(request, appLabel, modelName, object_id):
    try:
        Model = apps.get_model(appLabel, modelName)
        model_instance = get_object_or_404(Model, pk=object_id)
        verboseNamePlural = Model._meta.verbose_name_plural
        if request.method == 'POST':
            model_instance.delete()
            return redirect('datatable', appLabel=appLabel, modelName=modelName)

        context = {
            'model_instance': model_instance,
            'appLabel': appLabel,
            'modelName': modelName,
            'verboseNamePlural_value': verboseNamePlural,
        }
        context.update(getModelNames(appLabel))
        return render(request, 'datatable/delete.html', context)
    except Exception as err:
        return render(request, 'error.html', {'message': err})


def exportCsv(request, appLabel, modelName):
    try:
        Model = apps.get_model(appLabel, modelName)
        model_fields = [field.name for field in Model._meta.fields]
        objects = Model.objects.all()

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{modelName}.csv"'

        writer = csv.writer(response)
        writer.writerow(model_fields)

        for obj in objects:
            row = [getattr(obj, field) for field in model_fields]
            writer.writerow(row)

        return response
    except Exception as err:
        return render(request, 'error.html', {'message': err})


def importCsv(request, appLabel, modelName):
    try:
        Model = apps.get_model(appLabel, modelName)
        model_fields = [field.name for field in Model._meta.fields]
        verboseNamePlural = Model._meta.verbose_name_plural
        if request.method == 'POST' and request.FILES['csv_file']:
            csv_file = request.FILES['csv_file']
            reader = csv.reader(csv_file.read().decode('utf-8').splitlines())
            # next(reader)  # Skip header row

            for j, row in enumerate(reader, start=1):
                obj = Model()
                for i, field in enumerate(model_fields):
                    if field != 'EnableInd':
                        setattr(obj, field, row[i-1])
                # obj.pk = j
                obj.save()

            return redirect('datatable', appLabel=appLabel, modelName=modelName)

        context = {
            'appLabel': appLabel,
            'modelName': modelName,
            'verboseNamePlural_value': verboseNamePlural,
        }
        context.update(getModelNames(appLabel))
        return render(request, 'datatable/importCsv.html', context)
    except Exception as err:
        return render(request, 'error.html', {'message': err})
