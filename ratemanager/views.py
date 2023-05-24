import json
from pathlib import Path
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import os
import pandas as pd
from myproj.settings import BASE_DIR
from django.apps import apps
from .models import RatebookGroups, RateBooks, AllExhibits
from .forms import ViewRBForm
from django.utils.html import format_html


def rateManager(request):
    options = ['createRB', 'viewRB']
    appLabel = 'ratemanager'
    return render(request, 'ratemanager/home.html', locals())


def createRB(request):
    options = ['createRB', 'viewRB']
    appLabel = 'ratemanager'
    file_uploaded = False
    return render(request, 'ratemanager/ratebookmanager/create_rb.html', locals())


def uploadRB(request):
    options = ['createRB', 'viewRB']
    appLabel = 'ratemanager'
    msgs = []

    # save and get uploaded file path
    upfile = request.FILES.get('file')
    root = 'uploads'
    path = os.path.realpath(os.path.join(root, str(upfile.name)))
    fileexists = False
    if not fileexists:
        filstg = FileSystemStorage()
        upldfl = filstg.save(path, upfile)
        upldfl_url = filstg.url(upldfl)
    request.session['upload_url'] = upldfl_url

    # Function to find Ratebook Details Tab
    def findRBDetails(df):
        rateDetailsSheet = None
        for sheet in list(df.keys()):
            iLower = sheet.lower()
            if 'rate' in iLower and 'book' in iLower and 'details' in iLower:
                rateDetailsSheet = sheet
        return rateDetailsSheet

    file_uploaded = True
    sheet_name = None

    # read from excel file and convert to pandas series and HTML Table
    df = pd.read_excel('.'+request.session.get('upload_url'), sheet_name=None)
    sheet_name = findRBDetails(df)
    df = df[sheet_name]
    df = df.T.reset_index().T
    df_view = pd.Series(index=list(df[0]), data=list(df[1]), name='Details')
    rbDetilsTable = format_html(df_view.to_frame().to_html(justify='left', classes=['table', 'table-bordered']))
    request.session['rate_details'] = df_view.astype(str).to_dict()

    if sheet_name is not None:
        msgs.append('Found Ratebook Details')
    else:
        msgs.append('Could not find Ratebook Details \
                    Sheet in the uploaded Excel file please check again.')
    return render(request, 'ratemanager/ratebookmanager/create_rb.html', locals())


def loadRBtoDB(request):
    options = ['createRB', 'viewRB']
    appLabel = 'ratemanager'
    msgs = []
    loaded_to_db = False
    file_uploaded = True
    load_failed = False
    # get models from other apps
    uwCompany = apps.get_model('systemtables', 'uwcompany')
    state = apps.get_model('systemtables', 'state')
    carrier = apps.get_model('systemtables', 'carrier')
    lineOfBusiness = apps.get_model('systemtables', 'lineofbusiness')
    rate_details = request.session.get('rate_details')

    # Insert to DB (kind of validation automatically)
    try:
        SelectedCarrier = carrier.objects.get(CarrierName=rate_details['Carrier'])
        SelectedState = state.objects.get(StateName=rate_details['State'])
        SelectedLoB = lineOfBusiness.objects.get(LobName=rate_details['Line of Business'])
        SelectedCompany = uwCompany.objects.get(CompanyName=rate_details['UW Company'])
        getObj, loaded_to_db = RatebookGroups.objects.get_or_create(
            Carrier=SelectedCarrier,
            State=SelectedState,
            LoBusiness=SelectedLoB,
            UwCompany=SelectedCompany,
            ProductGroup=rate_details['Product Group'],
            ProductName=rate_details['Product Type'],
            ProductType=rate_details['Product Name'],
            ProjectID='Test Auto Generation',
            RatebookGroup='Test Auto Generation',
            RenewalEffDate=rate_details['Renewal Effective Date'],
            RenewalExpDate=rate_details['Renewal Expiry Date'],
            ActivationDate=rate_details['Activation Date'],
            ActivationTime=rate_details['Activation Time stamp']
        )
        if loaded_to_db:
            msgs.append('Sucessfully Loaded to Database.')
        else:
            msgs.append('Record already Exists, you may want to use update.')
            load_failed = True
    except Exception as err:
        load_failed = True
        msgs.append(err)
    return render(request, 'ratemanager/ratebookmanager/create_rb.html', locals())


def viewRB(request):
    options = ['createRB', 'viewRB']
    appLabel = 'ratemanager'
    form = ViewRBForm
    options = ['createRB', 'viewRB']
    appLabel = 'ratemanager'
    return render(request, "ratemanager/ratebookmanager/view_rb.html", locals())


def viewRatebooksTable(request):
    options = ['createRB', 'viewRB']
    appLabel = 'ratemanager'
    form = ViewRBForm
    SelectedID = request.POST.get('Exhibits')
    show_rb_table = True
    SelectedExhibit = AllExhibits.objects.get(pk=SelectedID).Exhibit
    print(SelectedExhibit)
    rb_df = pd.DataFrame.from_records(AllExhibits.objects.filter(
        Exhibit=SelectedExhibit).values()
        )
    rb_html = format_html(rb_df.to_html(index=False, justify='left', classes=['table', 'table-bordered']))
    return render(request, "ratemanager/ratebookmanager/view_rb.html", locals())


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
