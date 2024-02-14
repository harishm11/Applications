from django.shortcuts import render
import ratemanager.views.HelperFunctions as helperfuncs
from ratemanager.forms import searchCriteriaForm, ratesUploadForm
# from ratemanager.models.ratebookmetadata import RatebookMetadata
# from ratemanager.models.ratebooktemplate import RatebookTemplate

# from django.contrib import messages
# from django.utils import timezone
# from myproj.messages import RATE_MANAGER
# from ratemanager.views.configs import ENVIRONMENT_HIERARCHY


def rates(request):
    options = helperfuncs.SIDEBAR_OPTIONS
    appLabel = 'ratemanager'
    title = 'Rates Home'
    return render(request, 'ratemanager/rates/home.html',
                  {
                      'options': options,
                      'appLabel': appLabel,
                      'title': title,

                  })


def ratebook(request):
    options = helperfuncs.SIDEBAR_OPTIONS
    appLabel = 'ratemanager'
    title = 'Rates - Rate books'

    return render(request, 'ratemanager/rates/rateBooks.html',
                  {
                      'options': options,
                      'appLabel': appLabel,
                      'title': title,
                      'searchCriteriaForm': searchCriteriaForm
                  })


def upload(request):
    options = helperfuncs.SIDEBAR_OPTIONS
    appLabel = 'ratemanager'
    title = 'Rates-Upload'
    return render(request, 'ratemanager/rates/upload.html',
                  {
                      'options': options,
                      'appLabel': appLabel,
                      'title': title,
                      'ratesUploadForm': ratesUploadForm
                  })


def migrate(request):
    options = helperfuncs.SIDEBAR_OPTIONS
    appLabel = 'ratemanager'
    title = 'Rates-Migrate'
    return render(request, 'ratemanager/rates/migrate.html',
                  {
                      'options': options,
                      'appLabel': appLabel,
                      'title': title,

                  })


def review(request):
    options = helperfuncs.SIDEBAR_OPTIONS
    appLabel = 'ratemanager'
    title = 'Rates-Review'
    return render(request, 'ratemanager/rates/review.html',
                  {
                      'options': options,
                      'appLabel': appLabel,
                      'title': title,

                  })


def compare(request):
    options = helperfuncs.SIDEBAR_OPTIONS
    appLabel = 'ratemanager'
    title = 'Rates-Compare'
    return render(request, 'ratemanager/rates/compare.html',
                  {
                      'options': options,
                      'appLabel': appLabel,
                      'title': title,

                  })
