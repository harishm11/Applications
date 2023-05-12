import csv
from django.http import HttpResponse
from django.forms.models import modelform_factory
from django.apps import apps
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.forms import modelform_factory
from django import forms
from productconfigurator.forms import *


def get_model_names(app_label):
    options = []
    for model in apps.get_app_config(app_label).get_models():
        options.append(model.__name__)
    modelnames = {'options': options}
    return modelnames


def datatable(request, app_label, model_name):
    try:
        Model = apps.get_model(app_label, model_name)
        model_fields = [field.name for field in Model._meta.fields]

        verbose_name_plural = Model._meta.verbose_name_plural
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
            'verbose_name_plural_value': verbose_name_plural,
            'app_label': app_label,
            'model_name': model_name,
            'search_query': search_query,


        }
        context.update(get_model_names(app_label))

        return render(request, 'datatable/datatable.html', context)
    except Exception as err:
        return render(request, 'error.html', {'message': err})


def add_object(request, app_label, model_name):
    try:
        Model = apps.get_model(app_label, model_name)
        # or use 'exclude' if needed

        if model_name == 'product':
            form_obj = ProductForm(request.POST)
        else:
            form_obj = modelform_factory(Model, fields='__all__', widgets={
                'OpenBookStartDate': forms.DateInput(attrs={'type': 'date'}),
                'CloseBookEndDate': forms.DateInput(attrs={'type': 'date'}),
                'EffectiveDate': forms.DateInput(attrs={'type': 'date'}),
                'ExpiryDate': forms.DateInput(attrs={'type': 'date'}),
            })
        verbose_name_plural = Model._meta.verbose_name_plural
        if request.method == 'POST':
            if form_obj.is_valid():
                form_obj.save()
                return redirect('datatable', app_label=app_label, model_name=model_name)
        else:
            form = form_obj

        context = {
            'form': form,
            'app_label': app_label,
            'model_name': model_name,
            'verbose_name_plural_value': verbose_name_plural,
        }
        context.update(get_model_names(app_label))

        return render(request, 'datatable/add.html', context)
    except Exception as err:
        return render(request, 'error.html', {'message': err})


def edit_object(request, app_label, model_name, object_id):
    try:
        Model = apps.get_model(app_label, model_name)
        instance = get_object_or_404(Model, pk=object_id)
        # or use 'exclude' if needed
        form = modelform_factory(Model, fields='__all__')
        verbose_name_plural = Model._meta.verbose_name_plural
        if request.method == 'POST':
            form = form(request.POST, instance=instance)
            if form.is_valid():
                form.save()
                return redirect('datatable', app_label=app_label, model_name=model_name)

        context = {
            'form': form(instance=instance),
            'app_label': app_label,
            'model_name': model_name,
            'object_id': object_id,
            'verbose_name_plural_value': verbose_name_plural,
        }

        return render(request, 'datatable/edit.html', context)
    except Exception as err:
        return render(request, 'error.html', {'message': err})


def delete_object(request, app_label, model_name, object_id):
    try:
        Model = apps.get_model(app_label, model_name)
        model_instance = get_object_or_404(Model, pk=object_id)
        verbose_name_plural = Model._meta.verbose_name_plural
        if request.method == 'POST':
            model_instance.delete()
            return redirect('datatable', app_label=app_label, model_name=model_name)

        context = {
            'model_instance': model_instance,
            'app_label': app_label,
            'model_name': model_name,
            'verbose_name_plural_value': verbose_name_plural,
        }
        context.update(get_model_names(app_label))
        return render(request, 'datatable/delete.html', context)
    except Exception as err:
        return render(request, 'error.html', {'message': err})


def export_csv(request, app_label, model_name):
    try:
        Model = apps.get_model(app_label, model_name)
        model_fields = [field.name for field in Model._meta.fields]
        objects = Model.objects.all()

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{model_name}.csv"'

        writer = csv.writer(response)
        writer.writerow(model_fields)

        for obj in objects:
            row = [getattr(obj, field) for field in model_fields]
            writer.writerow(row)

        return response
    except Exception as err:
        return render(request, 'error.html', {'message': err})


def import_csv(request, app_label, model_name):
    try:
        Model = apps.get_model(app_label, model_name)
        model_fields = [field.name for field in Model._meta.fields]
        verbose_name_plural = Model._meta.verbose_name_plural
        if request.method == 'POST' and request.FILES['csv_file']:
            csv_file = request.FILES['csv_file']
            reader = csv.reader(csv_file.read().decode('utf-8').splitlines())
            # next(reader)  # Skip header row

            for j, row in enumerate(reader, start=1):
                obj = Model()
                for i, field in enumerate(model_fields):
                    setattr(obj, field, row[i-1])
                obj.pk = j
                obj.save()

            return redirect('datatable', app_label=app_label, model_name=model_name)

        context = {
            'app_label': app_label,
            'model_name': model_name,
            'verbose_name_plural_value': verbose_name_plural,
        }

        return render(request, 'datatable/import_csv.html', context, get_model_names(app_label))
    except Exception as err:
        return render(request, 'error.html', {'message': err})
