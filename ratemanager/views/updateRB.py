import traceback
import pandas as pd
from django.shortcuts import render
import ratemanager.views.HelperFunctions as helperfuncs
from ratemanager.forms import UpdateForm
from ratemanager.models import Ratebooks, AllExhibits
from datetime import datetime
from pandas.errors import EmptyDataError


def updateRB(request):
    options = helperfuncs.SIDEBAR_OPTIONS
    appLabel = "ratemanager"
    form = UpdateForm
    return render(request, "ratemanager/ratebookmanager/update_rb.html", locals())


def loadUpdatedRB(request):
    options = helperfuncs.SIDEBAR_OPTIONS
    appLabel = "ratemanager"
    # save the uploaded file from the form upload file and get form values
    uploadUrl = helperfuncs.uploadFile(request)
    file_uploaded = True
    msgs = []
    rbChangesTable = None
    loaded_to_db = False
    load_failed = False
    updateFormValues = {k: v[0] for k, v in dict(request.POST).items()}

    # read from excel file and find the Ratebook details Sheet
    df = pd.read_excel(uploadUrl, sheet_name=None, header=None)
    extractedRBDetails = helperfuncs.extractRatebookDetails(df)

    rate_details = extractedRBDetails['details_df'].astype(str).to_dict()
    rbDetailsTable = extractedRBDetails['details_html']
    msgs.extend(extractedRBDetails['msgs'])

    # modify and add to the rate details dictionary
    rate_details["RatebookRevisionType"] = "Rate Revision"
    rate_details["RatebookStatusType"] = "In Production"
    rate_details["RatebookChangeType"] = "Rate Revision"
    rate_details["CreationDateTime"] = datetime.now().strftime("%m-%d-%Y")

    rate_details = helperfuncs.fetchForeignFields(rate_details)
    rate_details = helperfuncs.applyDateConversion(rate_details)

    identityKeys = ("Carrier", "State", "LineofBusiness", "UWCompany",
                    "PolicyType", "PolicyType", "PolicySubType", "ProductCode")
    identityRateDetails = {key: rate_details.get(key) for key in identityKeys}

    # get last version RatebookID with similar details
    rbObjLastVersion = Ratebooks.objects.filter(**identityRateDetails).\
        order_by("-RatebookVersion").first()
    rate_details["RatebookID"] = (
        rbObjLastVersion.RatebookID if rbObjLastVersion is not None else None
    )

    def addMetadataToAllExhibitsRecord(Record, rate_details):
        Record["Ratebook_id"] = rbObj.id
        Record["RatebookVersion"] = rate_details["RatebookVersion"]
        Record["RatebookID"] = rate_details["RatebookID"]
        Record["RecordStatus"] = 'Active'
        for key in rate_details:
            if 'Date' in key or 'Time' in key:
                Record[key] = rate_details[key]

    def searchAllExhibitsRow(newRecord):
        identityKeys = ('RatebookID', 'Coverage', 'Exhibit',
                        'RatingVarName1', 'RatingVarValue1',
                        'RatingVarName2', 'RatingVarValue2')
        identityRateDetails = {key: newRecord.get(key) for key in identityKeys}
        identityRateDetails['RecordStatus'] = 'Active'
        # Get the specific row with given key
        searchObj = AllExhibits.objects.get(**identityRateDetails)
        return searchObj

    def expireAllExhibitsRow(Obj, newRecord: dict):
        ''' Expire a Old Record with dates from New Record '''
        Obj.NewBusinessExpiryDate = newRecord['NewBusinessEffectiveDate']
        Obj.RenewalExpiryDate = newRecord['RenewalEffectiveDate']
        Obj.RecordStatus = 'Expired'
        Obj.save()

    # if No similar ratebook found let the user know
    if rate_details["RatebookID"] is None:
        msgs.append("Unable to find any similar Ratebook. You may want to use Create.")
    else:
        if updateFormValues.get("RatebookUpdateType") == "minor":
            rate_details["RatebookVersion"] = rbObjLastVersion.RatebookVersion + 0.1
            rbObj, loaded_to_dbBooks = Ratebooks.objects.get_or_create(**rate_details)
        elif updateFormValues.get("RatebookUpdateType") == "major":
            rate_details["RatebookVersion"] = rbObjLastVersion.RatebookVersion + 1
            rbObj, loaded_to_dbBooks = Ratebooks.objects.get_or_create(**rate_details)

        loaded_to_dbExhibits = False
        if loaded_to_dbBooks:
            try:
                # transform the data from excel file to dataframe form
                df, errors = helperfuncs.transformRB(xl_url=uploadUrl)
                msgs.extend(errors)

                oldRB = helperfuncs.fetchRBLatestVersion(rate_details['RatebookID'])

                # filter only for exhibits in the new DF
                oldRB = oldRB.filter(Exhibit__in=df['Exhibit'].unique())

                oldRB = helperfuncs.convert2Df(oldRB)
                changes, stats = helperfuncs.dataframe_difference(old_df=oldRB, new_df=df)
                if stats['isEmpty']:
                    msgs.append('No Changes found.')
                    raise EmptyDataError
                rbChangesTable = helperfuncs.generate_html_diff(changes)

                # Add Rate Revised rows and expire the old Rate Rows
                for row in changes['modified'].itertuples(index=False):
                    Record = dict(row._asdict())
                    del Record['Factor_Old']
                    Record['Factor'] = Record['Factor_New']
                    del Record['Factor_New']
                    addMetadataToAllExhibitsRecord(Record=Record, rate_details=rate_details)
                    searchedObj = searchAllExhibitsRow(Record)
                    expireAllExhibitsRow(searchedObj, newRecord=Record)
                    AllExhibits.objects.create(**Record)
                # Expire the Deleted Rows
                for row in changes['deleted'].itertuples(index=False):
                    Record = dict(row._asdict())
                    addMetadataToAllExhibitsRecord(Record=Record, rate_details=rate_details)
                    searchedObj = searchAllExhibitsRow(Record)
                    expireAllExhibitsRow(searchedObj, newRecord=Record)
                # Add the newly added rows
                for row in changes['added'].itertuples(index=False):
                    Record = dict(row._asdict())
                    addMetadataToAllExhibitsRecord(Record=Record, rate_details=rate_details)
                    AllExhibits.objects.create(**Record)

                loaded_to_dbExhibits = True

            except Exception as err:
                traceback.print_exc()
                msgs.append(repr(err))
                loaded_to_dbExhibits = False
                if rbObj:
                    Ratebooks.objects.get(pk=rbObj.id).delete()

        else:
            msgs.append("Record already exists")

        if all([loaded_to_dbBooks, loaded_to_dbExhibits]):
            loaded_to_db = True
            msgs.append("Sucessfully Loaded to Database.")
        else:
            msgs.append("Unable to load to Database.")
            load_failed = True

    context = {
        'msgs': msgs,
        'load_failed': load_failed,
        'loaded_to_db': loaded_to_db,
        'rbDetailsTable': rbDetailsTable,
        'rbChangesTable': rbChangesTable,
        'file_uploaded': file_uploaded,
        'options': options,
        'appLabel': appLabel
    }
    return render(request, "ratemanager/ratebookmanager/update_rb.html", context)
