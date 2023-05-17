from django.shortcuts import render
from django.apps import apps
from .forms import *


def systemtables(request):
    options = []
    for model in apps.get_app_config('systemtables').get_models():
        options.append(model.__name__)
    context = {'options': options, 'appLabel': 'systemtables'}
    return render(request, 'systemtables/home.html', context)


def createModel(request):
    if request.method == 'POST':
        form = CreateModelForm(request.POST)
        if form.is_valid():
            form.saveModel()
    else:
        form = CreateModelForm()
    return render(request, 'systemtables/createModel.html', {'form': form})
