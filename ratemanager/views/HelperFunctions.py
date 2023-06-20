import pandas as pd
from datetime import datetime
from django.apps import apps
from ratemanager.models import Ratebooks


def transformRB(xl_url):
    ''' Function to transform the excel file to required form
    to be able to load into postgres database.'''

    msgs = []
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

    def get_table_category(sheet_name):
        if 'severitybands' in sheet_name.lower() or 'pointsassignment' in sheet_name.lower():
            return 'Miscellaneous'
        else:
            return 'Pricing'

    for sheet_name, df in df_sheets.items():

        # Categorize Tables based on column features and type of transformation
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
            df['TableCategory'] = get_table_category(sheet_name)

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
            df['TableCategory'] = get_table_category(sheet_name)

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
            df['TableCategory'] = get_table_category(sheet_name)

            df = df.astype(str)
            if not df.empty:
                df_out = pd.merge(df_out, df, how='outer')
            df_out = df_out.astype(str)

        elif table_sig == 'only coverages':
            df = df.T.reset_index()
            df.rename(columns={'index': 'Coverage', 0: 'Factor'}, inplace=True)
            df['Exhibit'] = sheet_name
            df['TableCategory'] = get_table_category(sheet_name)
            df = df.astype(str)
            if not df.empty:
                df_out = pd.merge(df_out, df, how='outer')
            df_out = df_out.astype(str)

    df_out = df_out[df_out.columns.sort_values().to_list()]
    df_out.replace('nan', '', regex=True, inplace=True)
    for i in set(df_sheets.keys()) - set(df_out['Exhibit'].unique()):
        msgs.append('Unable to transform {} table.'.format(i))

    return df_out, msgs


def convertDates(x):
    ''' converts date from mm-dd-yy to django acceptable format '''
    if '/' in x:
        return datetime.strptime(x, "%m/%d/%Y").strftime('%Y-%m-%d')
    elif '-' in x:
        return datetime.strptime(x, "%m-%d-%Y").strftime('%Y-%m-%d')


def applyDateConversion(rate_details):
    for key in rate_details:
        if 'Date' in key:
            rate_details[key] = convertDates(rate_details[key])
    return rate_details


def fetchForeignFields(rate_details):
    # get models from other apps
    uwCompany = apps.get_model('systemtables', 'uwcompany')
    state = apps.get_model('systemtables', 'state')
    carrier = apps.get_model('systemtables', 'carrier')
    lineOfBusiness = apps.get_model('systemtables', 'lineofbusiness')
    policyType = apps.get_model('systemtables', 'policytype')
    policySubType = apps.get_model('systemtables', 'policysubtype')
    productCode = apps.get_model('systemtables', 'productcode')
    rate_details['Carrier'] = carrier.objects.get(CarrierName=rate_details['Carrier'])
    rate_details['State'] = state.objects.get(StateName=rate_details['State'])
    rate_details['LineofBusiness'] = lineOfBusiness.objects.get(LobName=rate_details['LineofBusiness'])
    rate_details['UWCompany'] = uwCompany.objects.get(CompanyName=rate_details['UWCompany'])
    rate_details['PolicyType'] = policyType.objects.get(PolicyTypeName=rate_details['PolicyType'])
    rate_details['PolicySubType'] = policySubType.objects.get(PolicySubTypeName=rate_details['PolicySubType'])
    rate_details['ProductCode'] = productCode.objects.get(ProductCd=rate_details['ProductCode'])
    return rate_details


def generateRatebookID():
    LargestID = Ratebooks.objects.filter().order_by('-RatebookID').first().RatebookID
    if LargestID is not None:
        head = LargestID.rstrip('0123456789')
        tail = LargestID[len(head):]
        newrb = head + str(int(tail)+1).zfill(4)
        return newrb
    else:
        return 'RB0001'
