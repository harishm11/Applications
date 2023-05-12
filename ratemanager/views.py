import json
from pathlib import Path
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import os
from django.db import connection
import pandas as pd
import tabula
from myproj.settings import BASE_DIR
from django.apps import apps
from django.urls import get_resolver


def extractData(request):
    filepath = '/Users/harishmurali/insucompare/RateFiling doc1 - equity.pdf'
    outpath = '/Users/harishmurali/insucompare/RateFiling doc1 - equity.csv'
    tables = tabula.read_pdf(filepath, pages="all")

    # folder_name = "tables"
    # if not os.path.isdir(folder_name):
    #     os.mkdir(folder_name)
    # # iterate over extracted tables and export as excel individually
    # for i, table in enumerate(tables, start=1):
    #     table.to_excel(os.path.join(folder_name, f"table_{i}.xlsx"), index=False)

    dfs = tabula.read_pdf(filepath, pages='all')
    tabula.convert_into(filepath, outpath, output_format="csv", pages="all")


def uploadexhibit(request):
    state = apps.get_model('productconfigurator', 'state')
    states = state.objects.all()

    carrier = apps.get_model('productconfigurator', 'carrier')
    carriers = carrier.objects.all()
    return render(request, 'ratemanager/uploadexhibit.html', {'heading': 'Upload Exhibits file', 'states': states, 'carriers': carriers})


def uploadexhibitfile(request):
    try:
        upfile = request.FILES['file']
        root = 'uploads'
        path = os.path.realpath(os.path.join(root, str(upfile.name)))
        fileexists = False
        if not fileexists:
            filstg = FileSystemStorage()
            upldfl = filstg.save(path, upfile)
            upldfl_url = filstg.url(upldfl)
        return render(request, 'message.html', {'msg': 'File uplaoded'})
    except Exception as err:
        return render(request, 'message.html', {'msg': 'File not uplaoded'})


def exhibitlist(request):
    root = BASE_DIR
    file = 'uploads/CA Farmers Rating Factors (1).xlsx'
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
    file = 'CA Farmers Rating Factors (1).xlsx'
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


def ratemanager(request):
    options = []
    for url_pattern in get_resolver().url_patterns:
        if url_pattern.app_name == 'ratemanager':
            options.append(url_pattern.url_patterns.__name__)
    context = {'options': options, 'app_label': 'ratemanager'}
    return render(request, "ratemanager/home.html", context)
