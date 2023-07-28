import io
import pandas as pd
from django.http import FileResponse
import ratemanager.views.HelperFunctions as hf


def exportTemplate(request):
    obj_id_list = request.GET.getlist('selectedRBs')
    rbID, rbVer, _, _ = obj_id_list[0].split('_')
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
    pd.Series(
        index=export_details,
        ).to_excel(writer, sheet_name='Ratebook Details', index=True, header=None)
    pd.DataFrame(
        [], columns=['Deleted Exhibit Name']
        ).to_excel(writer, sheet_name='DELETED_EXHIBITS', index=False)
    pd.DataFrame(
        [], columns=['Old Exhibit Name', 'New Exhibit Name']
        ).to_excel(writer, sheet_name='RENAMED_EXHIBITS', index=False)
    for i in df['Exhibit'].unique():
        pd.DataFrame([], columns=['Exhibit Update Status', '(Modified/Added/Deleted/Renamed)'])\
            .to_excel(writer, sheet_name=i, index=False)

    writer.close()
    xl.seek(0)
    return FileResponse(xl, filename=obj_id_list[0]+'.xlsx')
