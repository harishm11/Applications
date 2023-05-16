import json
from pathlib import Path
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import os
from django.db import connection
import pandas as pd
from myproj.settings import BASE_DIR
from django.apps import apps
from .models import RatebookGroups, RateBooks, AllExhibits


def extractData(request):
    pass


def uploadexhibit(request):
    return render(request, 'ratemanager/uploadexhibit.html', {'heading': 'Upload Exhibit as excel file'})


def ratemanager(request):
    options = ['ratebookmanager', 'filterbyfield', 'viewratebookstable']

    context = {'options': options, 'appLabel': 'ratemanager'}
    return render(request, 'ratemanager/home.html', context)


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
        return render(request, 'ratemanager/uploadmessage.html', {'msg': 'File uploaded to ' + upldfl_url})
    except Exception:
        return render(request, 'ratemanager/uploadmessage.html', {'msg': 'File not uploaded'})


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


def ratebookmanager(request):
    bookgroup = RatebookGroups.objects.all()
    state = bookgroup.values_list('state', flat=True).distinct()
    business = []
    company = []
    product_group = []
    product_type = []
    product_name = []
    ratebookgroupid = []
    return render(request, "ratemanager/ratebookmanager/home.html", locals())


def filterbyfield(request):
    bookgroup = RatebookGroups.objects.all()
    state = bookgroup.values_list('state', flat=True).distinct()
    business = []
    company = []
    product_group = []
    product_type = []
    product_name = []
    ratebookgroupid = []

    stateid = request.GET.get('stateid')
    businessid = request.GET.get('businessid')
    companyid = request.GET.get('companyid')
    product_groupid = request.GET.get('product_groupid')
    product_typeid = request.GET.get('product_typeid')
    product_nameid = request.GET.get('product_nameid')
    book_groupid = request.GET.get('book_groupid')
    if len(stateid) != 0:
        business = RatebookGroups.objects.filter(
            state=stateid).values_list('business', flat=True).distinct()
        if len(businessid) != 0:
            company = RatebookGroups.objects.filter(state=stateid,
                                                    business=businessid).values_list('company', flat=True).distinct()
            if len(companyid) != 0:
                product_group = RatebookGroups.objects.filter(state=stateid,
                                                              business=businessid,
                                                              company=companyid).values_list('product_group', flat=True).distinct()
                if len(product_groupid) != 0:
                    product_type = RatebookGroups.objects.filter(state=stateid,
                                                                 business=businessid,
                                                                 company=companyid,
                                                                 product_group=product_groupid).values_list('product_type', flat=True).distinct()
                    if len(product_typeid) != 0:
                        product_name = RatebookGroups.objects.filter(state=stateid,
                                                                     business=businessid,
                                                                     company=companyid,
                                                                     product_group=product_groupid,
                                                                     product_type=product_typeid).values_list('product_name', flat=True).distinct()
                        if len(product_nameid) != 0:
                            ratebookgroupid = RatebookGroups.objects.filter(state=stateid,
                                                                            business=businessid,
                                                                            company=companyid,
                                                                            product_group=product_groupid,
                                                                            product_type=product_typeid,
                                                                            product_name=product_nameid).values_list('ratebookgroupid', flat=True).distinct()
    return render(request, "ratemanager/ratebookmanager/home.html", locals())


def viewratebookstable(request):
    book_groupid = request.POST.get('ratebookgroupid')
    print(book_groupid)
    rb_list = RateBooks.objects.all().filter(ratebookgroupid=book_groupid)
    print(rb_list)
    return render(request, "ratemanager/ratebookmanager/rb_table.html", locals())
