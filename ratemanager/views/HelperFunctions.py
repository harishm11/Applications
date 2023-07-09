import os
import pandas as pd
from datetime import datetime
from django.apps import apps
from ratemanager.models import Ratebooks, AllExhibits
from myproj.settings import BASE_DIR
from django.core.files.storage import FileSystemStorage
from django.db.models.expressions import Window
from django.db.models.functions import RowNumber
from django.db.models import Q, F

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
    for i in set(df_sheets.keys()) - set(df_out["Exhibit"].unique()):
        if i != "Ratebook Details":
            msgs.append("Unable to transform {} table.".format(i))

    return df_out, msgs


def convertDates(x):
    """converts date from mm-dd-yy to django acceptable format"""
    if "/" in x:
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
    # Raw Query
    """
    SELECT *
    FROM
    (
        SELECT *, ROW_NUMBER() OVER (PARTITION BY (
            t1."Coverage",
            t1."Exhibit",
            t1."RatingVarName1",
            t1."RatingVarValue1",
            t1."RatingVarName2",
            t1."RatingVarValue2")
        ORDER BY "RatebookVersion" DESC) AS sort_id
        FROM public."myTest" t1 WHERE "RatebookVersion" <= 4 -- (Parameter: Required Ratebook Version)
    ) AS Subquery
    WHERE sort_id = 1 and "RatebookID" = 'RB0001'; -- Required Ratebook
    """

    # equivalent django query
    sorted_partitions = AllExhibits.objects.filter(
        RatebookID=rbID, RatebookVersion__lte=rbVersion
    ).alias(
        sort_id=Window(
            expression=RowNumber(),
            partition_by=(
                F("Coverage"),
                F("Exhibit"),
                F("RatingVarName1"),
                F("RatingVarName2"),
                F("RatingVarValue1"),
                F("RatingVarValue2"),
            ),
            order_by=(F("RatebookVersion").desc()),
        )
    )
    current_version = sorted_partitions.filter(sort_id=1)
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
        & Q(ActivationDate__lte=qDate)
    )
    return filteredQueryResults
