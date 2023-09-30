from django.shortcuts import render, get_object_or_404
import ratemanager.views.HelperFunctions as helperfuncs
from ratemanager.models import RatebookMetadata
from ratemanager.forms import inputPKForm


def viewTemplate(request):
    options = helperfuncs.SIDEBAR_OPTIONS
    appLabel = 'ratemanager'

    if request.method == 'POST':
        obj = get_object_or_404(RatebookMetadata, pk=request.POST['pk'])
        TempleteObjectHeirarchy = dict()
        for i in obj.ratingexhibits_set.all():
            currentExhibitHeirarchy = dict()
            ratingVars = []
            for j in i.ratingvariables_set.all():
                ratingVars.append(j.DisplayName)
            currentExhibitHeirarchy['vars'] = ratingVars
            currentExhibitHeirarchy['covs'] = i.Coverages.all()
            TempleteObjectHeirarchy[i.Exhibit] = currentExhibitHeirarchy
        return render(request, 'ratemanager/viewTemplate.html',
                      {
                          'TempleteObjectHeirarchy': TempleteObjectHeirarchy,
                          'options': options,
                          'appLabel': appLabel
                      })
    if request.method == 'GET':
        form = inputPKForm()
        return render(request, 'ratemanager/inputPK.html',
                      {
                        'form': form,
                        'options': options,
                        'appLabel': appLabel
                      })
