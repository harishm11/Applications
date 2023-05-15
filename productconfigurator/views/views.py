
from ..forms import CreateModelForm
from django.forms import formset_factory
from django.http import HttpResponse
from django.db import migrations, models
from django.shortcuts import render
from django.utils.text import camel_case_to_spaces
from django.forms.models import model_to_dict
from django import forms
from django.db.models.base import ModelBase
from django.apps import apps
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db import models
from django.db import connection, migrations, models, transaction
from django.core.management import call_command
from django.db import DEFAULT_DB_ALIAS, connections
from django.core.management import execute_from_command_line


def productconfigurator(request):
    options = []
    for model in apps.get_app_config('productconfigurator').get_models():
        options.append(model.__name__)
    context = {'options': options, 'appLabel': 'productconfigurator'}
    return render(request, 'productconfigurator/home.html', context)


def createModel(request):
    if request.method == 'POST':
        form = CreateModelForm(request.POST)
        if form.is_valid():
            form.saveModel()
    else:
        form = CreateModelForm()
    return render(request, 'productconfigurator/createModel.html', {'form': form})
