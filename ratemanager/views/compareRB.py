import pandas as pd
from django.utils.html import format_html
from django.shortcuts import render
from ratemanager.views import HelperFunctions as hf


def compareRB(request):
    options = hf.SIDEBAR_OPTIONS
    appLabel = 'ratemanager'
    msgs = []
    diffTableHTML = 'No Changes Found.'
    statsTable = ''
    changedExhibits = ''

    obj_id_list = request.GET.getlist('selectedRBs')
    if obj_id_list is not None:
        obj_id_list = [x.split('_') for x in obj_id_list]
    compare_data = {}
    compare_data['RBID'] = obj_id_list[0][0]
    compare_data['new'] = max([float(obj_id_list[0][1]), float(obj_id_list[1][1])])
    compare_data['old'] = min([float(obj_id_list[0][1]), float(obj_id_list[1][1])])
    oldVerQs = hf.fetchRatebookSpecificVersion(compare_data['RBID'], compare_data['old'])
    newVerQs = hf.fetchRatebookSpecificVersion(compare_data['RBID'], compare_data['new'])
    oldVerDf = hf.convert2Df(oldVerQs)
    newVerDf = hf.convert2Df(newVerQs)
    changes, stats = hf.dataframe_difference(old_df=oldVerDf, new_df=newVerDf)

    if stats['isEmpty']:
        msgs.append('No Changes found.')
    else:
        del stats['isEmpty']
        diffTableHTML = hf.generate_html_diff(changes)

        changedExhibits = stats['changed_exhibits']
        del stats['changed_exhibits']
        statsTable = format_html(pd.Series(stats).to_frame().
                                 to_html(header=False, classes=["table table-bordered"]))

    context = {
        'diffTableHTML': diffTableHTML,
        'oldVer': compare_data['old'],
        'newVer': compare_data['new'],
        'rbID': compare_data['RBID'],
        'statsTableHTML': statsTable,
        'changedExhibits': changedExhibits,
        'options': options,
        'appLabel': appLabel
        }
    return render(request, "ratemanager/compareRB.html", context=context)
