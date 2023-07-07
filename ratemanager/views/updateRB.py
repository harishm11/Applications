import traceback
import pandas as pd
from django.shortcuts import render
import ratemanager.views.HelperFunctions as helperfuncs
from django.utils.html import format_html
from ratemanager.forms import UpdateForm
from ratemanager.models import Ratebooks, AllExhibits
from datetime import datetime


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
    updateFormValues = {k: v[0] for k, v in dict(request.POST).items()}

    # read from excel file and find the Ratebook details Sheet
    df = pd.read_excel(uploadUrl, sheet_name=None, header=None)
    sheet_name = helperfuncs.findRBDetails(df)

    if sheet_name is not None:
        msgs.append("Found Ratebook Details")
        df = df[sheet_name]
        df[0] = df[0].str.replace(" ", "")
        df_view = pd.Series(index=list(df[0]), data=list(df[1]), name="Details")
        df_view.astype(str).replace("nan", None, inplace=True)
        rbDetailsTable = format_html(
            df_view.to_frame().to_html(
                justify="left", classes=["table", "table-bordered"]
            )
        )
        rate_details = df_view.astype(str).to_dict()
    else:
        msgs.append(
            "Could not find Ratebook Details Sheet\
                     in the uploaded Excel file please check again."
        )

    rate_details["RatebookRevisionType"] = "Test"
    rate_details["RatebookStatusType"] = "Test"
    rate_details["RatebookChangeType"] = "Test"
    rate_details["CreationDateTime"] = datetime.now().strftime("%m-%d-%Y")
    rate_details = helperfuncs.fetchForeignFields(rate_details)
    rate_details = helperfuncs.applyDateConversion(rate_details)
    identityKeys = ("Carrier", "State", "LineofBusiness", "UWCompany",
                    "PolicyType", "PolicyType", "PolicySubType", "ProductCode")
    identityRateDetails = {key: rate_details.get(key) for key in identityKeys}

    # get last version RatebookID with similar details
    rbObjLastVersion = (
        Ratebooks.objects.filter(**identityRateDetails)
        .order_by("-RatebookVersion")
        .first()
    )
    rate_details["RatebookID"] = (
        rbObjLastVersion.RatebookID if rbObjLastVersion is not None else None
    )

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

                # code to load latest version from AllExhibits of given RBID as a dataframe
                oldRb = helperfuncs.fetchRatebookSpecificVersion(
                    rbID=rate_details["RatebookID"],
                    rbVersion=rate_details["RatebookVersion"],
                ).values_list()
                oldRB_df = pd.DataFrame.from_records(
                    oldRb,
                    columns=[
                        f.name
                        for f in AllExhibits._meta.get_fields(include_hidden=False)
                    ],
                ).drop(["id", "Ratebook", "RatebookID", "RatebookVersion"], axis=1)

                # find rows that are not in the new dataframe and add them to AllExhibits
                comparison_df = oldRB_df.merge(df, indicator=True, how="outer")
                diff_df = comparison_df.loc[comparison_df._merge == "right_only"]
                if diff_df.empty:
                    raise "Maybe not a new version as No Changes Found in the New Version."
                rbChangesTable = format_html(
                    diff_df.to_html(justify="left", classes=["table", "table-bordered"])
                )
                for row in (diff_df.drop("_merge", axis=1).itertuples(index=False)):
                    Record = dict(row._asdict())
                    Record["Ratebook_id"] = rbObj.id
                    Record["RatebookVersion"] = rate_details["RatebookVersion"]
                    Record["RatebookID"] = rate_details["RatebookID"]

                    for key in rate_details:
                        if "Date" in key or "Time" in key:
                            if "Expiry" not in key:
                                Record[key] = rate_details[key]
                            else:
                                Record[key] = None

                    identityKeys = ('Coverage', 'Exhibit',
                                    'RatingVarName1', 'RatingVarValue1',
                                    'RatingVarName2', 'RatingVarValue2')
                    identityRateDetails = {key: Record.get(key) for key in identityKeys}
                    searchObj = AllExhibits.objects.get(**identityRateDetails)
                    if searchObj.Factor != Record['Factor']:
                        searchObj.NewBusinessExpiryDate = Record['NewBusinessEffectiveDate']
                        searchObj.RenewalExpiryDate = Record['RenewalEffectiveDate']
                        searchObj.save()
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

    return render(request, "ratemanager/ratebookmanager/update_rb.html", locals())
