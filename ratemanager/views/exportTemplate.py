import io
import pandas as pd
from django.http import FileResponse
import ratemanager.views.HelperFunctions as hf
from ratemanager.models import Ratebooks
from django.apps import apps


def exportTemplate(request):
    obj_id_list = request.GET.getlist('selectedRBs')
    rbID, rbVer, _, _ = obj_id_list[0].split('_')
    rbMeta = Ratebooks.objects.filter(RatebookID=rbID, RatebookVersion=rbVer).values()[0]
    requiredRbQS = hf.fetchRatebookSpecificVersion(rbID=rbID, rbVersion=rbVer)
    df = hf.convert2Df(requiredRbQS)
    xl = io.BytesIO()
    writer = pd.ExcelWriter(xl, engine='xlsxwriter')

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
        'Migration Time',
        'Project ID'
    ]
    print(rbMeta)
    data = []
    for x in export_details:
        toIn = rbMeta.get(x.replace(' ', ''))
        if toIn:
            data.append(toIn)
        else:
            model = apps.get_model("systemtables", x.replace(' ', '').lower())
            data.append(model.objects.get(pk=rbMeta.get(x.replace(' ', '')+'_id')))

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
