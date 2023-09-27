from django.shortcuts import render
import ratemanager.views.HelperFunctions as helperfuncs


def viewTemplate(request):
    options = helperfuncs.SIDEBAR_OPTIONS
    appLabel = 'ratemanager'

    return render(request, 'ratemanager/viewTemplate.html',
                  {
                      'options': options,
                      'appLabel': appLabel
                  })
