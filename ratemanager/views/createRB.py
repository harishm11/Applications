import os
import traceback
import pandas as pd
import sqlalchemy as sa
from django.shortcuts import render
from myproj.settings import BASE_DIR, DATABASES
from ratemanager.models import Ratebooks
from ratemanager.forms import UpdateForm
from django.utils.html import format_html
from django.core.files.storage import FileSystemStorage
import ratemanager.views.HelperFunctions as helperfuncs


def createRB(request):
    options = ['createRB', 'viewRB']
    appLabel = 'ratemanager'
    file_uploaded = False
    load_failed = False
    form = UpdateForm
    return render(request, 'ratemanager/ratebookmanager/create_rb.html', locals())


def uploadRB(request):
    options = ['createRB', 'viewRB']
    appLabel = 'ratemanager'
    msgs = []

    request.session['updateform'] = {k: v[0] for k, v in dict(request.POST).items()}

    # save and get uploaded file path
    upfile = request.FILES.get('file')
    root = os.path.join(BASE_DIR, 'uploads')
    path = os.path.abspath(os.path.join(root, str(upfile.name.replace(' ', ''))))
    fileexists = False
    if not fileexists:
        filstg = FileSystemStorage(base_url=str(BASE_DIR))
        upldfl = filstg.save(path, upfile)
        upldfl_url = filstg.url(upldfl)
    request.session['upload_url'] = upldfl_url
    file_uploaded = True

    def findRBDetails(df):
        ''' Function to find Ratebook Details Tab '''

        rateDetailsSheet = None
        for sheet in list(df.keys()):
            iLower = sheet.lower()
            if 'rate' in iLower and 'book' in iLower and 'details' in iLower:
                rateDetailsSheet = sheet
        return rateDetailsSheet

    # read from excel file and convert to pandas series and HTML Table
    df = pd.read_excel(request.session.get('upload_url'), sheet_name=None, header=None)
    sheet_name = findRBDetails(df)

    if sheet_name is not None:
        msgs.append('Found Ratebook Details')
        df = df[sheet_name]
        df[0] = df[0].str.replace(' ', '')
        df_view = pd.Series(index=list(df[0]), data=list(df[1]), name='Details')
        rbDetailsTable = format_html(df_view.to_frame().to_html(justify='left', classes=['table', 'table-bordered']))
        request.session['rate_details'] = df_view.astype(str).to_dict()
        request.session['rate_book'] = df.astype(str).to_dict()
    else:
        msgs.append('Could not find Ratebook Details Sheet\
                     in the uploaded Excel file please check again.')

    return render(request, 'ratemanager/ratebookmanager/create_rb.html', locals())


def loadRBtoDB(request):
    options = ['createRB', 'viewRB']
    appLabel = 'ratemanager'
    msgs = []
    loaded_to_db = False
    file_uploaded = True
    load_failed = False
    rate_details = request.session.get('rate_details')
    updateFormValues = request.session.get('updateform')

    try:
        loaded_to_dbBooks = False
        rbObj = None
        rate_details['RatebookRevisionType'] = 'Test'
        rate_details['RatebookStatusType'] = 'Test'
        rate_details['RatebookChangeType'] = 'Test'
        rate_details = helperfuncs.fetchForeignFields(rate_details)
        rate_details = helperfuncs.applyDateConversion(rate_details)
        identityKeys = ('Carrier', 'State', 'LineofBusiness', 'UWCompany', 'PolicyType',
                        'PolicyType', 'PolicySubType', 'ProductCode')
        identityRateDetails = {key: rate_details.get(key) for key in identityKeys}

        if updateFormValues.get('RatebookCreationType') == 'new':
            rate_details['RatebookVersion'] = 0.0
            rate_details['RatebookID'] = helperfuncs.generateRatebookID()
            if Ratebooks.objects.filter(**identityRateDetails).count() == 0:
                rbObj, loaded_to_dbBooks = Ratebooks.objects.get_or_create(**rate_details)
            else:
                msgs.append('Another Ratebook with similar details already exists\
                            You may want to use Update.')

        elif updateFormValues.get('RatebookCreationType') == 'update':
            rbObjLastVersion = Ratebooks.objects.filter(**identityRateDetails).order_by('-RatebookVersion').first()
            rate_details['RatebookID'] = rbObjLastVersion.RatebookID
            if updateFormValues.get('RatebookUpdateType') == 'minor':
                rate_details['RatebookVersion'] = rbObjLastVersion.RatebookVersion + 0.1
                rbObj, loaded_to_dbBooks = Ratebooks.objects.get_or_create(**rate_details)
            elif updateFormValues.get('RatebookUpdateType') == 'major':
                rate_details['RatebookVersion'] = rbObjLastVersion.RatebookVersion + 1
                rbObj, loaded_to_dbBooks = Ratebooks.objects.get_or_create(**rate_details)

        loaded_to_dbExhibits = False
        if loaded_to_dbBooks:
            try:
                # create connection to database
                db_url = 'postgresql://' + DATABASES['default']['USER'] + ':' \
                        + DATABASES['default']['PASSWORD'] + '@'\
                        + DATABASES['default']['HOST'] + ':'\
                        + DATABASES['default']['PORT'] + '/'\
                        + DATABASES['default']['NAME']
                engine = sa.create_engine(db_url)
                # transform the data to usable form
                df, errors = helperfuncs.transformRB(xl_url=request.session['upload_url'])
                msgs.extend(errors)
                df['Ratebook_id'] = rbObj.id
                # load to Database
                df.to_sql('ratemanager_allexhibits', engine, method='multi', if_exists='append', index=False)
                loaded_to_dbExhibits = True
            except Exception as err:
                traceback.print_exc()
                msgs.append(repr(err))
                loaded_to_dbExhibits = False
                if rbObj:
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
