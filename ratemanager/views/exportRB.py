import io
import pandas as pd
from django.http import FileResponse
import ratemanager.views.HelperFunctions as hf
from ratemanager.models.ratebookmetadata import RatebookMetadata
from ratemanager.models.ratebooktemplate import RatebookTemplate

from django.apps import apps
from django.shortcuts import render
from ratemanager.forms import exportRBForm
import ratemanager.views.configs as configs


def exportRB(request):
    options = hf.SIDEBAR_OPTIONS
    appLabel = 'ratemanager'

    export_details = configs.export_details
    if request.method == 'GET':
        obj_id_list = request.GET.getlist('selectedRBs')
        rbID, rbVer, rbState, rbCode = obj_id_list[0].split('_')
        requiredRbQS = hf.fetchRatebookSpecificVersion(rbID=rbID, rbVersion=rbVer)
        form = exportRBForm()
        CHOICES = requiredRbQS.all().values_list('Exhibit', flat=True).distinct()
        form.fields['toExportExhibits'].choices = ((x, ' '.join(hf.camel_case_split(x))) for x in CHOICES)
        return render(request, 'ratemanager/exportRB.html',
                      {
                        'form': form,
                        'options': options,
                        'appLabel': appLabel,
                        'rbID': rbID,
                        'rbVer': rbVer,
                        'rbState': rbState,
                        'rbCode': rbCode
                        })
    if request.method == 'POST':
        rbID, rbVer = request.POST['rbID'], request.POST['rbVer']
        rbMeta = RatebookMetadata.objects.filter(RatebookID=rbID, RatebookVersion=rbVer)
        if rbMeta:
            rbMeta = rbMeta.values()[0]
        else:
            raise Exception('Ratebook not found')
        requiredRbQS = hf.fetchRatebookSpecificVersion(rbID=rbID, rbVersion=rbVer)
        df = hf.convert2Df(requiredRbQS)
        xl = io.BytesIO()
        writer = pd.ExcelWriter(xl, engine='xlsxwriter')

        data = []
        for x in export_details:
            toIn = rbMeta.get(x.replace(' ', ''))
            if toIn:
                data.append(toIn)
            else:
                model = apps.get_model("systemtables", x.replace(' ', '').lower())
                if model.__name__ == 'State':
                    data.append(model.objects.get(pk=rbMeta.get(x.replace(' ', '')+'_id')).StateName)
                else:
                    data.append(model.objects.get(pk=rbMeta.get(x.replace(' ', '')+'_id')))

        pd.Series(index=export_details,
                  data=data
                  ).to_excel(writer, sheet_name='Ratebook Details', index=True, header=None)
        pd.DataFrame(
            [], columns=['Deleted Exhibit Name']
            ).to_excel(writer, sheet_name='DELETED_EXHIBITS', index=False)
        for i in request.POST.getlist('toExportExhibits'):
            hf.inverseTransform(df[df['Exhibit'] == i]).to_excel(writer, sheet_name=i, index=False)

        writer.close()
        xl.seek(0)
        return FileResponse(xl, filename='_'.join([str(rbID), str(rbVer), str(request.POST['rbState']), str(request.POST['rbCode']), '.xlsx']))


def exportTemplate(request, pk):
    rbMeta = RatebookMetadata.objects.filter(RatebookID=pk).order_by('-RatebookVersion')
    exbList = RatebookTemplate.objects.filter(RatebookID=pk)
    rbMeta = rbMeta.values()[0]
    export_details = configs.export_details

    xl = io.BytesIO()
    writer = pd.ExcelWriter(xl, engine='xlsxwriter')

    # write the ratebook details to the excel file
    data = []
    for x in export_details:
        toIn = rbMeta.get(x.replace(' ', ''))
        if toIn:
            data.append(toIn)
        else:
            try:
                model = apps.get_model("systemtables", x.replace(' ', '').lower())
                if model.__name__ == 'State':
                    data.append(model.objects.get(pk=rbMeta.get(x.replace(' ', '')+'_id')).StateName)
                else:
                    data.append(model.objects.get(pk=rbMeta.get(x.replace(' ', '')+'_id')))
            except LookupError:
                data.append(None)
                continue

    pd.Series(index=export_details,
              data=data
              ).to_excel(writer, sheet_name='Ratebook Details', index=True, header=None)

    # write only the selected exhibits to the excel file
    for i in exbList:
        rvs = i.ExhibitVariables.all()
        cols = [rv.DisplayName for rv in rvs]
        cols.extend(i.ExhibitCoverages.all())
        pd.DataFrame(
            data=[], columns=cols
        ).to_excel(writer, sheet_name=i.RatebookExhibit.Exhibit, index=False)

    writer.close()
    xl.seek(0)
    filename = '_'.join(list(map(str, [rbMeta['RatebookID'], rbMeta['RatebookName'], '.xlsx'])))
    return FileResponse(xl, filename=filename, as_attachment=True)
