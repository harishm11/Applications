import os
import pandas as pd
from datetime import datetime
from django.apps import apps
from ratemanager.models import Ratebooks, AllExhibits
from myproj.settings import BASE_DIR
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.utils.html import format_html
from copy import deepcopy

SIDEBAR_OPTIONS = ["createRB", "viewRB", "updateRB"]


def transformRB(xl_url):
    """Function to transform the excel file to required form
    to be able to load into postgres database."""

    msgs = []
    df_sheets = pd.read_excel(xl_url, sheet_name=None)
    df_out = pd.DataFrame(columns=["Exhibit", "Coverage", "Factor"])

    def create_rate_vars_cols(df, var_list):
        rename_col_names = []
        for i in range(1, len(var_list) + 1):
            rename_col_names.append((var_list[i - 1], "RatingVarValue" + str(i)))
        rename_col_names = dict(rename_col_names)
        for i in range(1, len(var_list) + 1):
            df["RatingVarName" + str(i)] = var_list[i - 1]
        df.rename(columns=rename_col_names, inplace=True)

    def get_table_category(sheet_name):
        if (
            "severitybands" in sheet_name.lower()
            or "pointsassignment" in sheet_name.lower()
        ):
            return "Miscellaneous"
        else:
            return "Pricing"

    for sheet_name, df in df_sheets.items():
        # Categorize Tables based on column features and type of transformation
        idvars = []
        table_sig = ""
        for i in df.columns:
            if df.columns[0] == "BI":
                table_sig = "only coverages"
            elif i == "Coverage":
                table_sig = "coverage as rows"
                break
            elif "UMPD" not in sheet_name and not any(
                [
                    (x == i or (x in i and "Symbol" not in i))
                    for x in ["BI", "COMP", "PD", "UM", "UMBI", "MED", "COLL", "Factor"]
                ]
            ):
                table_sig = "coverage as columns"
                idvars.append(i)
            else:
                break

        # handle transformation based on each category
        if table_sig == "coverage as columns":
            df = df.melt(id_vars=idvars)
            create_rate_vars_cols(df, idvars)
            df.rename(columns={"variable": "Coverage", "value": "Factor"}, inplace=True)
            df["Exhibit"] = sheet_name
            df["TableCategory"] = get_table_category(sheet_name)

            df = df.astype(str)
            if not df.empty:
                df_out = pd.merge(df_out, df, how="outer")
            df_out = df_out.astype(str)

        elif table_sig == "coverage as rows":
            df.rename(columns={"Factor Amt.": "Factor"}, inplace=True)
            rate_vars = []
            for i in df.columns:
                if i != "Factor" and i != "Coverage":
                    rate_vars.append(i)
            create_rate_vars_cols(df, rate_vars)
            df["Exhibit"] = sheet_name
            df["TableCategory"] = get_table_category(sheet_name)

            df = df.astype(str)
            if not df.empty:
                df_out = pd.merge(df_out, df, how="outer")
            df_out = df_out.astype(str)

        elif "UMPD" in sheet_name:
            idvars = []
            for i in df.columns:
                if i == "Deductible":
                    idvars.append(i)
            df = df.melt(id_vars=idvars)
            df.rename(
                columns={"variable": "Description", "value": "Factor"}, inplace=True
            )
            create_rate_vars_cols(df, list(set(df.columns) - set({"Factor"})))
            df["Exhibit"] = sheet_name
            df["Coverage"] = "UMPD"
            df["TableCategory"] = get_table_category(sheet_name)

            df = df.astype(str)
            if not df.empty:
                df_out = pd.merge(df_out, df, how="outer")
            df_out = df_out.astype(str)

        elif table_sig == "only coverages":
            df = df.T.reset_index()
            df.rename(columns={"index": "Coverage", 0: "Factor"}, inplace=True)
            df["Exhibit"] = sheet_name
            df["TableCategory"] = get_table_category(sheet_name)
            df = df.astype(str)
            if not df.empty:
                df_out = pd.merge(df_out, df, how="outer")
            df_out = df_out.astype(str)

    numRatingVars = 2
    for i in range(1, numRatingVars+1):
        if 'RatingVarName' + str(i) not in df_out.columns:
            df_out['RatingVarName' + str(i)] = None
            df_out['RatingVarValue' + str(i)] = None

    df_out = df_out[df_out.columns.sort_values().to_list()]
    df_out = df_out.astype(object).replace('nan', None, regex=True)
    for i in set(df_sheets.keys()) - set(df_out["Exhibit"].unique()):
        if i != "Ratebook Details" or i != 'Rate Details':
            msgs.append("Unable to transform {} table.".format(i))

    return df_out, msgs


def convertDates(x):
    """converts date from mm-dd-yy to django acceptable format"""
    if ':' in x:
        return datetime.strptime(x, "%Y-%d-%m %H:%M:%S").strftime("%Y-%m-%d")
    elif "/" in x:
        return datetime.strptime(x, "%m/%d/%Y").strftime("%Y-%m-%d")
    elif "-" in x:
        return datetime.strptime(x, "%m-%d-%Y").strftime("%Y-%m-%d")


def applyDateConversion(rate_details):
    ''' apply date conversion from m/d/y to django required format'''
    for key in rate_details:
        if "Date" in key:
            rate_details[key] = convertDates(rate_details[key])
    return rate_details


def fetchForeignFields(rate_details):
    ''' This function fetches the foreign key field objects in ratebook details while creating a ratebook. '''
    # get models from other apps
    uwCompany = apps.get_model("systemtables", "uwcompany")
    state = apps.get_model("systemtables", "state")
    carrier = apps.get_model("systemtables", "carrier")
    lineOfBusiness = apps.get_model("systemtables", "lineofbusiness")
    policyType = apps.get_model("systemtables", "policytype")
    policySubType = apps.get_model("systemtables", "policysubtype")
    productCode = apps.get_model("systemtables", "productcode")
    rate_details["Carrier"] = carrier.objects.get(CarrierName=rate_details["Carrier"])
    rate_details["State"] = state.objects.get(StateName=rate_details["State"])
    rate_details["LineofBusiness"] = lineOfBusiness.objects.get(
        LobName=rate_details["LineofBusiness"]
    )
    rate_details["UWCompany"] = uwCompany.objects.get(
        CompanyName=rate_details["UWCompany"]
    )
    rate_details["PolicyType"] = policyType.objects.get(
        PolicyTypeName=rate_details["PolicyType"]
    )
    rate_details["PolicySubType"] = policySubType.objects.get(
        PolicySubTypeName=rate_details["PolicySubType"]
    )
    rate_details["ProductCode"] = productCode.objects.get(
        ProductCd=rate_details["ProductCode"]
    )
    return rate_details


def generateRatebookID():
    ''' This function generates a Ratebook ID of the format "RB00XX" by incrementing the existing largest ID '''
    LargestIDObj = Ratebooks.objects.filter().order_by("-RatebookID").first()
    LargestID = LargestIDObj.RatebookID if LargestIDObj is not None else None
    if LargestID is not None:
        head = LargestID.rstrip("0123456789")
        tail = LargestID[len(head):]
        newrb = head + str(int(tail) + 1).zfill(4)
        return newrb
    else:
        return "RB0001"


def loadtoAllExhibits(df):
    ''' This function loads a Dataframe to AllExhibits Model '''
    for row in df.itertuples(index=False):
        Record = dict(row._asdict())
        AllExhibits.objects.create(**Record)


def findRBDetails(df):
    """ Function to find Ratebook Details Tab
        returns ratebook details sheet name """

    rateDetailsSheet = None
    for sheet in list(df.keys()):
        iLower = sheet.lower()
        if ("rate" in iLower or "book" in iLower) and "details" in iLower:
            rateDetailsSheet = sheet
    return rateDetailsSheet


def uploadFile(request):
    ''' Function to get the uploaded file from request and save it.
        returns the file path url. '''
    # save and get uploaded file path
    upfile = request.FILES.get("file")
    root = os.path.join(BASE_DIR, "uploads")
    path = os.path.abspath(os.path.join(root, str(upfile.name.replace(" ", ""))))
    fileexists = False
    if not fileexists:
        filstg = FileSystemStorage(base_url=str(BASE_DIR))
        upldfl = filstg.save(path, upfile)
        upldfl_url = filstg.url(upldfl)
    return upldfl_url


def fetchRatebookSpecificVersion(rbID, rbVersion):

    ActivationDate = Ratebooks.objects.get(
        RatebookID=rbID,
        RatebookVersion=rbVersion
        ).ActivationDate

    current_version = fetchRatebookbyDate(rbID, ActivationDate)

    return current_version


def fetchRatebookbyDate(rbID, qDate):
    '''
    Select RATEBOOKID from Ratemanager_allexhibits
    where NB Effective <= current date
    and RN Effective Dt < = current Date
    and (( NB expiry and rn Expiry  is null)
    or (NB expiry and RN expiry date > current date) )
    and activation date <= current date
    '''
    filteredQueryResults = AllExhibits.objects.filter(RatebookID=rbID).filter(
        Q(NewBusinessEffectiveDate__lte=qDate)
        & Q(RenewalEffectiveDate__lt=qDate)
        & (
            (Q(NewBusinessExpiryDate__isnull=True) & Q(RenewalExpiryDate__isnull=True))
            | (Q(NewBusinessExpiryDate__gt=qDate) & Q(RenewalExpiryDate__gt=qDate))
        )
        & (Q(ActivationDate__lte=qDate))
    )
    return filteredQueryResults


def buildViewFilterQuery(selected: dict):
    '''
    Builds a query joined by '&' on Carrier, State, Company
    Business, Policy Type, Sub Type, Product Code.

    'selected' is a dictionay containing the request data of filter form.
    '''
    rbQuery = Q()
    if selected.get('Carrier') != '' and selected.get('Carrier') is not None:
        rbQuery &= Q(Carrier_id=selected.get('Carrier'))
    if selected.get('StateCode') != '' and selected.get('StateCode') is not None:
        rbQuery &= Q(State_id=selected.get('StateCode'))
    if selected.get('UwCompany') != '' and selected.get('UwCompany') is not None:
        rbQuery &= Q(UwCompany_id=selected.get('UwCompany'))
    if selected.get('LineofBusiness') != '' and selected.get('LineofBusiness') is not None:
        rbQuery &= Q(LineofBusiness_id=selected.get('LineofBusiness'))
    if selected.get('PolicyType') != '' and selected.get('PolicyType') is not None:
        rbQuery &= Q(PolicyType_id=selected.get('PolicyType'))
    if selected.get('PolicySubType') != '' and selected.get('PolicySubType') is not None:
        rbQuery &= Q(PolicySubType_id=selected.get('PolicySubType'))
    if selected.get('ProductCode') != '' and selected.get('ProductCode') is not None:
        rbQuery &= Q(ProductCode_id=selected.get('ProductCode'))

    return rbQuery


def extractRatebookDetails(inputDataFrame):
    df = inputDataFrame
    msgs = []
    sheet_name = findRBDetails(df)

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
    else:
        msgs.append("Could not find Ratebook Details Sheet\
                     in the uploaded Excel file please check again.")
    return {'details_html': rbDetailsTable,
            'details_df': df_view,
            'msgs': msgs}


def fetchRBLatestVersion(rbID):
    '''
    Loads latest version from AllExhibits of given RBID as a dataframe.
    '''
    latestVersion = (
        Ratebooks.objects.filter(RatebookID=rbID)
        .order_by("-RatebookVersion")
        .first()
    ).RatebookVersion
    oldRB = fetchRatebookSpecificVersion(
        rbID=rbID,
        rbVersion=latestVersion,
    )
    return oldRB


def dataframe_difference(old_df, new_df):
    """Find rows which are added, deleted or modified in the new version of DataFrame."""
    def convertToObject(df):
        ''' convert all columns to object dtype except factor '''
        for col in list(df.columns):
            if 'factor' not in col.lower():
                df[col] = df[col].astype(object)
        return df

    old_df = convertToObject(old_df)
    new_df = convertToObject(new_df)

    comparison_df = old_df.merge(
        new_df,
        indicator=True,
        how='outer'
    )

    deleted_old = comparison_df.loc[comparison_df._merge == 'left_only']
    added_new = comparison_df.loc[comparison_df._merge == 'right_only']

    modified = deleted_old.merge(
        added_new,
        how='inner',
        on=[x for x in list(new_df.columns) if x not in ('Factor', '_merge')]
    )
    modified.drop(['_merge_x', '_merge_y'], inplace=True, axis=1)
    modified.rename(columns={'Factor_x': 'Factor_Old',
                             'Factor_y': 'Factor_New'},
                    inplace=True)
    modified = modified[modified.columns.sort_values().to_list()]
    added_deleted = comparison_df.drop_duplicates(
        subset=[x for x in list(new_df.columns) if x not in ('Factor', '_merge')],
        ignore_index=True,
        keep=False
        )

    added = added_deleted.loc[added_deleted._merge == 'right_only'].drop('_merge', axis=1)
    deleted = added_deleted.loc[added_deleted._merge == 'left_only'].drop('_merge', axis=1)

    stats = {}
    stats['Number of rate revisions'] = len(modified)
    stats['Number of added factors'] = len(added)
    stats['Number of deleted factors'] = len(deleted)
    stats['changed_exhibits'] = []
    stats['changed_exhibits'].extend(added['Exhibit'].unique())
    stats['changed_exhibits'].extend(deleted['Exhibit'].unique())
    stats['changed_exhibits'].extend(modified['Exhibit'].unique())
    stats['changed_exhibits'] = set(stats['changed_exhibits'])
    stats['isEmpty'] = False if len(modified)+len(added)+len(deleted) > 0 else True

    return {'modified': modified,
            'added': added,
            'deleted': deleted,
            }, stats


def generate_html_diff(changes):
    ''' Generate Details about the changes in between the 2 dataframes '''
    updates = deepcopy(changes)
    updates['modified']['Factor'] = updates['modified']['Factor_Old'].astype(str) +\
        ' -> ' + updates['modified']['Factor_New'].astype(str)
    updates['modified'].drop(['Factor_Old', 'Factor_New'], axis=1, inplace=True)
    updates['modified'] = updates['modified'][updates['modified'].columns.sort_values().to_list()]
    updates['added'] = updates['added'][updates['modified'].columns.sort_values().to_list()]
    updates['deleted'] = updates['deleted'][updates['modified'].columns.sort_values().to_list()]
    updates['modified'] = updates['modified'].astype(str).style.applymap(
        lambda x: "background-color: lightblue" if '->' in x else "background-color: white")
    updates['added'] = updates['added'].astype(str).style.applymap(
        lambda x: "background-color: lightgreen")
    updates['deleted'] = updates['deleted'].astype(str).style.applymap(
        lambda x: "background-color: lightcoral")
    diff_df = updates['modified'].concat(updates['deleted'])
    diff_df = diff_df.concat(updates['added'])
    diff_df = diff_df.hide(axis='index')
    rbChangesTableHTML = diff_df.to_html(
        table_uuid='changes'
        )
    return rbChangesTableHTML


def convert2Df(QuerySet):
    ''' Convert QuerySet to Dataframe and
    Drops fields not needed for comparision of Rate Factors '''
    toDropList = ['id', 'RatebookID', 'Ratebook_id', "RatebookVersion", "RecordStatus"]
    for i in [f.name for f in AllExhibits._meta.get_fields(include_hidden=False)]:
        if 'Date' in i or 'Time' in i:
            toDropList.extend([i])
    df = pd.DataFrame.from_records(QuerySet.values())
    if not df.empty:
        df.drop(columns=toDropList, axis=1, inplace=True)
    return df
