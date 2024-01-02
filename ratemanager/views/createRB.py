import traceback
import pandas as pd
from django.shortcuts import render
from ratemanager.models.ratebookmetadata import RatebookMetadata
from django.utils.html import format_html
import ratemanager.views.HelperFunctions as helperfuncs
from django.utils import timezone


def createRB(request):
    options = helperfuncs.SIDEBAR_OPTIONS
    appLabel = 'ratemanager'
    file_uploaded = False
    load_failed = False
    return render(request, 'ratemanager/ratebookmanager/create_rb.html', locals())


def uploadNewRB(request):
    options = helperfuncs.SIDEBAR_OPTIONS
    appLabel = 'ratemanager'
    msgs = []

    request.session['upload_url'] = helperfuncs.uploadFile(request)
    file_uploaded = True

    # read from excel file and convert to pandas series and HTML Table
    df = pd.read_excel(request.session.get('upload_url'),
                       sheet_name=None, header=None)
    sheet_name = helperfuncs.findRBDetails(df)

    if sheet_name is not None:
        msgs.append('Found Ratebook Details')
        df = df[sheet_name]
        df[0] = df[0].str.replace(' ', '')
        df_view = pd.Series(index=list(
            df[0]), data=list(df[1]), name='Details')
        rbDetailsTable = format_html(
            df_view.to_frame().to_html(
                justify='left', classes=['table', 'table-bordered']
            )
        )
        request.session['rate_details'] = df_view.astype(str).to_dict()

    else:
        msgs.append('Could not find Ratebook Details Sheet\
                     in the uploaded Excel file please check again.')

    return render(request, 'ratemanager/ratebookmanager/create_rb.html', locals())


def loadNewRBtoDB(request):
    options = helperfuncs.SIDEBAR_OPTIONS
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
        rate_details['ProjectID'] = 'Test'
        rate_details['RatebookRevisionType'] = 'Initial'
        rate_details['RatebookStatusType'] = 'In Production'
        rate_details['RatebookChangeType'] = 'Initial'
        rate_details['CreationDateTime'] = timezone.now().strftime('%m-%d-%Y')
        rate_details = helperfuncs.fetchForeignFields(rate_details)
        rate_details = helperfuncs.applyDateConversion(rate_details)

        identityKeys = ('Carrier', 'State', 'LineofBusiness', 'UWCompany', 'PolicyType',
                        'PolicyType', 'PolicySubType', 'ProductCode')
        identityRateDetails = {
            key: rate_details.get(key) for key in identityKeys}

        rate_details['RatebookVersion'] = 0.0
        rate_details['RatebookID'] = helperfuncs.generateRatebookID()
        if RatebookMetadata.objects.filter(**identityRateDetails).count() == 0:
            rbObj, loaded_to_dbBooks = RatebookMetadata.objects.get_or_create(
                **rate_details)
        else:
            msgs.append('Another Ratebook with similar details already exists\
                        You may want to use Update.')

        loaded_to_dbExhibits = False
        if loaded_to_dbBooks:
            try:
                # transform the data to usable form
                df, errors = helperfuncs.transformRB(
                    xl_url=request.session['upload_url'])
                msgs.extend(errors)

                # update the rating exhibits and rating variables
                helperfuncs.updateRatingExhibits(
                    df, rbid=rbObj.id, uploadURL=request.session["upload_url"]
                )
                df['Ratebook_id'] = rbObj.id
                df['RatebookVersion'] = rate_details['RatebookVersion']
                df['RatebookID'] = rate_details['RatebookID']
                df['RecordStatus'] = 'Active'

                for key in rate_details:
                    if 'Date' in key or 'Time' in key:
                        df[key] = rate_details[key]

                helperfuncs.loadtoRatingFactors(df)
                loaded_to_dbExhibits = True

            except Exception as err:
                traceback.print_exc()
                msgs.append(repr(err))
                loaded_to_dbExhibits = False
                if rbObj:
                    RatebookMetadata.objects.get(pk=rbObj.id).delete()

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
