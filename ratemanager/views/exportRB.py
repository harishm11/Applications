import io
import pandas as pd
from django.http import FileResponse
import ratemanager.views.HelperFunctions as hf
from ratemanager.models import RatebookMetadata, RatingExhibits, RatingVariables
from django.apps import apps

export_details = [
    'Carrier',
    'State',
    'Line of Business',
    'Policy Type',
    'Policy Sub Type',
    'Product Code',
    'UW Company',
    'New Business Effective Date',
    'Renewal Effective Date',
    'Activation Date',
    'Activation Time',
    'Migration Date',
    'Migration Time'
]


def exportRB(request):
    obj_id_list = request.GET.getlist('selectedRBs')
    rbID, rbVer, _, _ = obj_id_list[0].split('_')
    rbMeta = RatebookMetadata.objects.filter(RatebookID=rbID, RatebookVersion=rbVer).values()[0]
    requiredRbQS = hf.fetchRatebookSpecificVersion(rbID=rbID, rbVersion=rbVer)
    df = hf.convert2Df(requiredRbQS)
    xl = io.BytesIO()
    writer = pd.ExcelWriter(xl, engine='xlsxwriter')

    data = []
    for x in export_details:
        toIn = rbMeta.get(x.replace(' ', ''))
        if toIn:
            data.append(toIn)
        elif 'projectid' not in x.lower():
            model = apps.get_model("systemtables", x.replace(' ', '').lower())
            data.append(model.objects.get(pk=rbMeta.get(x.replace(' ', '')+'_id')))
    data.append(rbMeta['ProjectID'])
    export_details.append('Project ID')
    pd.Series(index=export_details,
              data=data
              ).to_excel(writer, sheet_name='Ratebook Details', index=True, header=None)
    pd.DataFrame(
        [], columns=['Deleted Exhibit Name']
        ).to_excel(writer, sheet_name='DELETED_EXHIBITS', index=False)
    for i in df['Exhibit'].unique():
        hf.inverseTransform(df[df['Exhibit'] == i]).to_excel(writer, sheet_name=i, index=False)

    writer.close()
    xl.seek(0)
    return FileResponse(xl, filename=obj_id_list[0]+'.xlsx')


def exportTemplate(request, pk):
    rbMeta = RatebookMetadata.objects.filter(pk=pk)
    exbList = RatingExhibits.objects.filter(Ratebook=rbMeta[0])
    rbMeta = rbMeta.values()[0]

    xl = io.BytesIO()
    writer = pd.ExcelWriter(xl, engine='xlsxwriter')

    data = []
    for x in export_details:
        toIn = rbMeta.get(x.replace(' ', ''))
        if toIn:
            data.append(toIn)
        else:
            model = apps.get_model("systemtables", x.replace(' ', '').lower())
            data.append(model.objects.get(pk=rbMeta.get(x.replace(' ', '')+'_id')))
    data.append(rbMeta['ProjectID'])
    export_details.append('Project ID')
    pd.Series(index=export_details,
              data=data
              ).to_excel(writer, sheet_name='Ratebook Details', index=True, header=None)

    for i in exbList:
        rvs = RatingVariables.objects.filter(Exhibit=i).values()
        cols = [rv['RatingVarName'] for rv in rvs]
        cols.extend(i.Coverages)
        pd.DataFrame(
            data=[], columns=cols
        ).to_excel(writer, sheet_name=i.Exhibit, index=False)

    writer.close()
    xl.seek(0)
    filename = '_'.join(list(map(str, [rbMeta['RatebookID'], rbMeta['State_id'], rbMeta['ProductCode_id'], '.xlsx'])))
    return FileResponse(xl, filename=filename)
