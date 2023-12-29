import json
from pathlib import Path
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import os
import pandas as pd
from myproj.settings import BASE_DIR
import ratemanager.views.HelperFunctions as helperfuncs
from django.forms import modelformset_factory
from django.apps import apps

coverage = apps.get_model('systemtables', 'coverage')


def rateManager(request):
    options = helperfuncs.SIDEBAR_OPTIONS
    appLabel = 'ratemanager'
    return render(request, 'ratemanager/home.html', locals())


def exhibitlist(request):
    root = BASE_DIR
    file = 'uploads/Farmers.xlsx'
    # file = 'CA Farmers Rating Factors(1).xlsx'
    filepath = os.path.join(root, Path(file))
    xl = pd.ExcelFile(filepath)
    sheets = xl.sheet_names
    # xl.parse(sheet_name)
    return render(request, 'ratemanager/exhlist.html', {'sheets': sheets, 'title': file, 'heading': 'Select an Exhibit'})


def openfiling(request, data):
    root = 'uploads'
    shtname = data
    # filepath = request.META['PATH_INFO']
    file = 'Farmers.xlsx'
    filepath = os.path.join(root, Path(file))
    request.session['fp'] = str(filepath)
    request.session['sn'] = str(shtname)
    return render(request, 'ratemanager/exhibit.html', {'title': file.strip('xlsx'), 'heading': shtname})


def openexhibit(request):
    try:
        root = ''
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        os.chdir('../')
        file = request.session['fp']
        sheet = request.session['sn']
        filepath = os.path.join(root, file)
        out = pd.read_excel(filepath, sheet_name=sheet)
        out = out.sort_values(out.columns[0])
        out.columns = out.columns.str.replace('', '')
        out = out.fillna(" ")
        out = out.dropna()
        json_records = out.reset_index(drop=True).to_json(orient='records')
        data = json.loads(json_records)
        mylist = []
        for x in data:
            mylist.append(x)
        cols = mylist[0].keys()
        columns = []
        for i in cols:
            columns.append({
                'data': i,
                'name': i
            })
        response = {
            "data": mylist, 'columns': columns
        }
        return HttpResponse(JsonResponse(response))
    except Exception as err:
        response = HttpResponse(json.dumps(
            {'Error': err}), content_type='application/json')
        response.status_code = 400
        return response


# view to edit the Coverage records
def EditCoverages(request):
    # Get all instances of RatingCoverages
    my_objects = RatingCoverages.objects.all()

    # Create a formset for RatingCoverages instances
    RatingCoveragesFormSet = modelformset_factory(coverage, fields=('__all__'), can_delete=True, extra=0)
    formset = RatingCoveragesFormSet(queryset=my_objects)

    if request.method == 'POST':
        # Process the formset data
        formset = RatingCoveragesFormSet(request.POST, queryset=my_objects)
        if formset.is_valid():
            formset.save()
            return redirect('ratemanager:EditCoverages')

    return render(request, 'ratemanager/editCoverages.html', {'form': formset})
