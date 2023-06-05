import json
from pathlib import Path
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import os
import pandas as pd
from myproj.settings import BASE_DIR
from django.apps import apps
from ratemanager.models import Ratebooks, AllExhibits
from ratemanager.forms import ViewRBForm, SelectExhibitForm
from django.utils.html import format_html
import sqlalchemy as sa
from django.db.models import Q
import traceback
from datetime import datetime

# get models from other apps
uwCompany = apps.get_model('systemtables', 'uwcompany')
state = apps.get_model('systemtables', 'state')
carrier = apps.get_model('systemtables', 'carrier')
lineOfBusiness = apps.get_model('systemtables', 'lineofbusiness')
policyType = apps.get_model('systemtables', 'policytype')
policySubType = apps.get_model('systemtables', 'policysubtype')
productCode = apps.get_model('systemtables', 'productcode')


def rateManager(request):
    options = ['createRB', 'viewRB']
    appLabel = 'ratemanager'
    return render(request, 'ratemanager/home.html', locals())


def createRB(request):
    options = ['createRB', 'viewRB']
    appLabel = 'ratemanager'
    file_uploaded = False
    load_failed = False
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

    def findRBDetails(df):
        ''' Function to find Ratebook Details Tab '''

        rateDetailsSheet = None
        for sheet in list(df.keys()):
            iLower = sheet.lower()
            if 'rate' in iLower and 'book' in iLower and 'details' in iLower:
                rateDetailsSheet = sheet
        return rateDetailsSheet

    file_uploaded = True
    sheet_name = None

    # read from excel file and convert to pandas series and HTML Table
    df = pd.read_excel('.'+request.session.get('upload_url'), sheet_name=None, header=None)
    sheet_name = findRBDetails(df)
    df = df[sheet_name]
    df_view = pd.Series(index=list(df[0]), data=list(df[1]), name='Details')
    rbDetilsTable = format_html(df_view.to_frame().to_html(justify='left', classes=['table', 'table-bordered']))
    request.session['rate_details'] = df_view.astype(str).to_dict()
    request.session['rate_book'] = df.astype(str).to_dict()

    # def validate_fields(model, in_df):
    #     ''' Takes model name and input pandas dataframe and compares the fields/columns
    #     to validate the field names and whether all fields are present or not.'''

    #     errMsgs = []
    #     print(model._meta.get_fields())
    #     fields = [f.name for f in model._meta.get_fields(include_hidden=False)]
    #     print(fields)

    #     return True, errMsgs
    #
    # validated, errorMessages = validate_fields(RatebookGroups, df)
    # if validated:
    #     pass

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
    rate_details = request.session.get('rate_details')

    def transform(rbID, xl_url='.'+request.session['upload_url']):
        ''' Function to transform the excel file to required form
        to be able to load into postgres database.'''

        df_sheets = pd.read_excel(xl_url, sheet_name=None)
        df_out = pd.DataFrame(columns=['Exhibit', 'Coverage', 'Factor'])

        def create_rate_vars_cols(df, var_list):
            rename_col_names = []
            for i in range(1, len(var_list)+1):
                rename_col_names.append((var_list[i-1], 'RatingVarValue'+str(i)))
            rename_col_names = dict(rename_col_names)
            for i in range(1, len(var_list)+1):
                df['RatingVarName'+str(i)] = var_list[i-1]
            df.rename(columns=rename_col_names, inplace=True)

        for sheet_name, df in df_sheets.items():
            # Categorize Tables based on column features
            idvars = []
            table_sig = ''
            for i in df.columns:
                if df.columns[0] == 'BI':
                    table_sig = 'only coverages'
                elif i == 'Coverage':
                    table_sig = 'coverage as rows'
                    break
                elif 'UMPD' not in sheet_name and not any([(x == i or (x in i and 'Symbol' not in i)) for x in ['BI', 'COMP', 'PD', 'UM', 'UMBI', 'MED', 'COLL', 'Factor']]):
                    table_sig = 'coverage as columns'
                    idvars.append(i)
                else:
                    break

            # handle transformation based on each category
            if table_sig == 'coverage as columns':

                df = df.melt(id_vars=idvars)
                create_rate_vars_cols(df, idvars)
                df.rename(columns={'variable': 'Coverage', 'value': 'Factor'}, inplace=True)
                df['Exhibit'] = sheet_name

                df = df.astype(str)
                if not df.empty:
                    df_out = pd.merge(df_out, df, how='outer')
                df_out = df_out.astype(str)

            elif table_sig == 'coverage as rows':

                df.rename(columns={'Factor Amt.': 'Factor'}, inplace=True)
                rate_vars = []
                for i in df.columns:
                    if (i != 'Factor' and i != 'Coverage'):
                        rate_vars.append(i)
                create_rate_vars_cols(df, rate_vars)
                df['Exhibit'] = sheet_name

                df = df.astype(str)
                if not df.empty:
                    df_out = pd.merge(df_out, df, how='outer')
                df_out = df_out.astype(str)

            elif 'UMPD' in sheet_name:
                idvars = []
                for i in df.columns:
                    if (i == 'Deductible'):
                        idvars.append(i)
                df = df.melt(id_vars=idvars)
                df.rename(columns={'variable': 'Description', 'value': 'Factor'}, inplace=True)
                create_rate_vars_cols(df, list(set(df.columns)-set({'Factor'})))
                df['Exhibit'] = sheet_name
                df['Coverage'] = 'UMPD'

                df = df.astype(str)
                if not df.empty:
                    df_out = pd.merge(df_out, df, how='outer')
                df_out = df_out.astype(str)

            elif table_sig == 'only coverages':
                df = df.T.reset_index()
                df.rename(columns={'index': 'Coverage', 0: 'Factor'}, inplace=True)
                df['Exhibit'] = sheet_name
                df = df.astype(str)
                if not df.empty:
                    df_out = pd.merge(df_out, df, how='outer')
                df_out = df_out.astype(str)

        df_out = df_out[df_out.columns.sort_values().to_list()]
        df_out.replace('nan', '', regex=True, inplace=True)
        df_out['Ratebook_id'] = rbID
        for i in set(df_sheets.keys()) - set(df_out['Exhibit'].unique()):
            msgs.append('Unable to transform {} table.'.format(i))

        return df_out

    def convertDate(x):
        return datetime.strptime(x, "%m/%d/%Y").strftime('%Y-%m-%d')

    # Insert to DB (kind of validation automatically from the error messages)
    try:
        SelectedCarrier = carrier.objects.get(CarrierName=rate_details['Carrier'])
        SelectedState = state.objects.get(StateName=rate_details['State'])
        SelectedLoB = lineOfBusiness.objects.get(LobName=rate_details['Line of Business'])
        SelectedCompany = uwCompany.objects.get(CompanyName=rate_details['UW Company'])
        SelectedPolicyType = policyType.objects.get(PolicyTypeName=rate_details['Policy Type'])
        SelectedPolicySubType = policySubType.objects.get(PolicySubTypeName=rate_details['Policy Sub Type'])
        SelectedProductCode = productCode.objects.get(ProductCd=rate_details['Product Code'])
        rbObj, loaded_to_dbBooks = Ratebooks.objects.get_or_create(
            Carrier=SelectedCarrier,
            State=SelectedState,
            LoBusiness=SelectedLoB,
            UwCompany=SelectedCompany,
            PolicyType=SelectedPolicyType,
            ProductCode=SelectedProductCode,
            PolicySubType=SelectedPolicySubType,
            ProjectID='Test Auto Generation',
            NewBusinessEffectiveDate=convertDate(rate_details['New Business Effective Date']),
            NewBusinessExpiryDate=convertDate(rate_details['New Business Expiry Date']),
            RenewalEffectiveDate=convertDate(rate_details['Renewal Effective Date']),
            RenewalExpiryDate=convertDate(rate_details['Renewal Expiry Date']),
            ActivationDate=convertDate(rate_details['Activation Date']),
            ActivationTime=rate_details['Activation Time'],
            MigrationDate=convertDate(rate_details['Migration Date']),
            MigrationTime=rate_details['Migration Time'],
            RatebookVersion=0,
            RatebookRevisionType='Test',
            RatebookStatusType='Test',
            RatebookChangeType='Test'
        )

        loaded_to_dbExhibits = False
        if loaded_to_dbBooks:
            try:
                # create connection to database
                db_url = 'postgresql://postgres:readonly@localhost:5432/postgres'
                engine = sa.create_engine(db_url)
                # transform the data to usable form
                df = transform(rbObj.id)
                # load to Database
                df.to_sql('ratemanager_allexhibits', engine, method='multi', if_exists='append', index=False)
                loaded_to_dbExhibits = True
            except Exception as err:
                msgs.append(repr(err))
                loaded_to_dbExhibits = False
                Ratebooks.objects.get(pk=rbObj.id).delete()
        else:
            msgs.append('Record already exists')

        if all([loaded_to_dbBooks, loaded_to_dbExhibits]):
            loaded_to_db = True
            msgs.append('Sucessfully Loaded to Database.')
        else:
            msgs.append('Unable to load to Database.')
            load_failed = True
    except Exception as err:
        load_failed = True
        msgs.append(err)
        traceback.print_exc()
    return render(request, 'ratemanager/ratebookmanager/create_rb.html', locals())


def viewRB(request):
    options = ['createRB', 'viewRB']
    appLabel = 'ratemanager'
    fields = [f.name for f in Ratebooks._meta.get_fields(include_hidden=False)][1:]
    if request.method == 'GET':
        viewForm = ViewRBForm
        filteredRatebooks = Ratebooks.objects.filter()
    if request.method == 'POST':
        selected = {k: v[0] for k, v in dict(request.POST).items()}

        rbQuery = Q()
        if selected.get('Carrier') != '':
            rbQuery &= Q(Carrier_id=selected.get('Carrier'))
        if selected.get('StateCode') != '':
            rbQuery &= Q(State_id=selected.get('StateCode'))
        if selected.get('UwCompany') != '':
            rbQuery &= Q(UwCompany_id=selected.get('UwCompany'))
        if selected.get('LineOfBusiness') != '':
            rbQuery &= Q(LoBusiness_id=selected.get('LineOfBusiness'))
        if selected.get('PolicyType') != '':
            rbQuery &= Q(PolicyType_id=selected.get('PolicyType'))
        if selected.get('PolicySubType') != '':
            rbQuery &= Q(PolicySubType_id=selected.get('PolicySubType'))
        if selected.get('ProductCode') != '':
            rbQuery &= Q(ProductCode_id=selected.get('ProductCode'))
        filteredRatebooks = Ratebooks.objects.filter(rbQuery)
        viewForm = ViewRBForm(initial=selected)
    return render(request, "ratemanager/ratebookmanager/view_rb.html", locals())


def viewExhibits(request, rbID):
    options = ['createRB', 'viewRB']
    appLabel = 'ratemanager'
    if request.method == 'GET':
        filteredExhibits = AllExhibits.objects.filter().values_list()
        fields = [f.name for f in AllExhibits._meta.get_fields(include_hidden=False)]
        exhibitForm = SelectExhibitForm
    if request.method == 'POST':
        selected = {k: v[0] for k, v in dict(request.POST).items()}
        Query = Q()
        Query &= Q(Ratebook_id=rbID)
        if selected.get('Exhibit') != '':
            Query &= Q(Exhibit=selected.get('Exhibit'))
        filteredExhibits = AllExhibits.objects.filter(Query).values_list()
        fields = [f.name for f in AllExhibits._meta.get_fields(include_hidden=False)]
        exhibitForm = SelectExhibitForm(initial=selected)
    return render(request, "ratemanager/ratebookmanager/view_exhibits.html", locals())


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
