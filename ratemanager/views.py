import json
from pathlib import Path
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import os
from django.db import connection
import pandas as pd
from myproj.settings import BASE_DIR
from django.apps import apps
from .models import RatebookGroups, RateBooks, AllExhibits
from .forms import ViewRBForm
from django.utils.html import format_html


def extractData(request):
    pass


def rateManager(request):
    options = ['ratebookManager', 'filterbyfield', 'viewRatebooksTable']
    appLabel = 'ratemanager'
    return render(request, 'ratemanager/home.html', locals())


def createFromExcel(request):
    try:
        show_result = True
        upfile = request.FILES['file']
        root = 'uploads'
        path = os.path.realpath(os.path.join(root, str(upfile.name)))
        fileexists = False
        if not fileexists:
            filstg = FileSystemStorage()
            upldfl = filstg.save(path, upfile)
            upldfl_url = filstg.url(upldfl)
        msg = 'File uploaded to path:' + upldfl_url + ' sucessfully.'
        err = ''
        df = pd.read_excel('.'+upldfl_url, sheet_name=None)

        # Function to find Ratebook Details Tab
        def findRBDetails(df):
            sheet = None
            for i in list(df.keys()):
                iLower = i.lower()
                if 'rate' in iLower and 'book' in iLower and 'details' in iLower:
                    sheet = i
            return sheet

        sheet_name = findRBDetails(df)
        df = df[sheet_name]
        df = df.T.reset_index().T
        df = df.T
        df, df.columns = df[1:], df.iloc[0]
        rbDetilsTable = format_html(df.to_html(index=False, justify='left', classes=['table', 'table-bordered']))
        if sheet_name is not None:
            msg = rbDetilsTable
        else:
            msg = 'Could not find Ratebook Details Sheet in the uploaded Excel file please check again.'
        return render(request, 'ratemanager/ratebookmanager/uploadmessage.html', locals())
    except Exception as err:
        return render(request, 'ratemanager/ratebookmanager/uploadmessage.html', {'msg': 'File not uploaded', 'err': err})


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


def ratebookManager(request):
    form = ViewRBForm
    options = ['ratebookManager', 'filterbyfield', 'viewRatebooksTable']
    appLabel = 'ratemanager'
    return render(request, "ratemanager/ratebookmanager/home.html", locals())


def viewRatebooksTable(request):
    form = ViewRBForm
    bookGroupID = request.POST.get('ratebookgroupid')
    print(bookGroupID)
    show_rb_table = True
    rb_df = pd.DataFrame.from_records(RateBooks.objects.all().values())
    rb_df.reset_index(inplace=True)
    rb_html = format_html(rb_df.to_html(index=False, justify='left', classes=['table', 'table-bordered']))
    return render(request, "ratemanager/ratebookmanager/home.html", locals())
