from ratemanager.forms import createTemplateForm, projectIdAndDateInputForm
from django.shortcuts import render, redirect
import ratemanager.views.HelperFunctions as helperfuncs
from ratemanager.models.ratebookmetadata import RatebookMetadata
from ratemanager.models.ratebooktemplate import RatebookTemplate

from django.contrib import messages
from django.utils import timezone
from myproj.messages import RATE_MANAGER
from ratemanager.views.configs import ENVIRONMENT_HIERARCHY


def template(request):
    options = helperfuncs.SIDEBAR_OPTIONS
    appLabel = 'ratemanager'

    # Left overs 'id', 'Environment', 'isDeleted', 'onHold', 'retrofitReq', 'Carrier', 'State', 'LineofBusiness', 'UWCompany', 'PolicyType', 'PolicySubType', 'ProductCode', 'NewBusinessExpiryDate', 'RenewalExpiryDate', 'CreationDateTime'
    searchResultTableHeadersNamesOrder = ['RatebookName', 'RatebookID',
                                          'RatebookVersion',  'RatebookStatusType',
                                          'NewBusinessEffectiveDate',  'RenewalEffectiveDate',
                                          ]
    fieldsDict = {x.name: x for x in RatebookMetadata._meta.fields}
    searchResultTableHeaders = [fieldsDict[field] for field in searchResultTableHeadersNamesOrder]

    form = createTemplateForm()

    # save the Form data to session before validation and main action
    if request.method == 'POST':
        ratebook_details = request.POST.copy()
        request.session['TemplateFormData'] = ratebook_details
        form = createTemplateForm(ratebook_details)

    # Required for GET requests
    if request.method == 'GET' and request.session.get('TemplateFormData'):
        form = createTemplateForm(
            request.session['TemplateFormData']
        )

    # Mostly the form will only be valid if it is a POST request
    if form.is_valid():
        # save the cleaned Form data to session
        form_data = form.cleaned_data

        # check for existing template/Ratebook in production and if found show that it already exists.
        identityDetails = helperfuncs.extractIdentityDetails(form_data)
        searchResults = RatebookMetadata.objects.filter(
                **identityDetails).order_by('-RatebookID')
        if 'Create a new Ratebook/Template' == request.POST.get('submit'):
            return redirect('ratemanager:projectIdAndDateInput')
        if searchResults.count() > 0 or request.POST.get('submit') == 'Search':

            # check for matching drafts if found show the draft.
            if searchResults.filter(RatebookStatusType='Initial Draft').count() > 0:
                messages.add_message(
                    request, messages.INFO, RATE_MANAGER['MES_0001'])
            elif searchResults.count() > 0:
                messages.add_message(
                    request, messages.INFO, RATE_MANAGER['MES_0002'])
            else:
                messages.add_message(
                    request, messages.INFO, RATE_MANAGER['MES_0003'])

            searchResults.order_by(
                'RatebookID', 'RatebookStatusType', '-RatebookVersion'
            ).distinct('RatebookID', 'RatebookStatusType')

        return render(request, 'ratemanager/Template.html',
                      {
                        'createTemplateForm': form,
                        'options': options,
                        'appLabel': appLabel,
                        'title': 'Template',
                        'searchResults': searchResults,
                        'searchResultTableHeaders': searchResultTableHeaders,
                        'ENVIRONMENT_HIERARCHY': ENVIRONMENT_HIERARCHY
                        })
    else:
        messages.add_message(request, messages.ERROR,
                             RATE_MANAGER['MES_0006'])
        return render(request, 'ratemanager/Template.html',
                      {
                        'createTemplateForm': form,
                        'options': options,
                        'appLabel': appLabel,
                        'title': 'Template',
                        })


def projectIdAndDateInput(request):
    options = helperfuncs.SIDEBAR_OPTIONS
    appLabel = 'ratemanager'

    def fetchDisplayData(searchOptions):
        cd = searchOptions.cleaned_data
        searchOptionsData = {
            searchOptions.fields[key].label: cd[key]
            for key in ('State', 'PolicyType', 'PolicySubType', 'ProductCode')
            }
        return searchOptionsData

    if request.method == 'GET':
        initial = {
            'NewBusinessEffectiveDate': timezone.now().date(),
            'RenewalEffectiveDate': timezone.now().date(),
            'ActivationDate': timezone.now().date(),
            'ActivationTime': timezone.now(),
            'MigrationDate': timezone.now().date(),
            'MigrationTime': timezone.now()
        }
        rbID = request.GET.get('rbID')
        form = projectIdAndDateInputForm(initial=initial)
        searchOptions = createTemplateForm(
                data=request.session.get('TemplateFormData') or request.session.get('PreviousSearchCriteria'))
        if searchOptions.is_valid():
            searchOptionsData = fetchDisplayData(searchOptions)
        return render(request, 'ratemanager/ProjectIdAndDateInput.html',
                      {
                          'options': options,
                          'appLabel': appLabel,
                          'form': form,
                          'title': 'Project ID & Dates',
                          'searchOptionsData': searchOptionsData,
                          'rbID': rbID,
                      })

    if request.method == 'POST':
        # save the forms data to RB meta data table
        searchOptions = createTemplateForm(
            data=request.session['TemplateFormData'])
        if searchOptions.is_valid():
            searchOptionsData = fetchDisplayData(searchOptions)
        form = projectIdAndDateInputForm(request.POST)
        rbID = request.POST.get('rbID')
        if form.is_valid():
            form_data = form.cleaned_data
            form_data.update(
                searchOptions.cleaned_data
            )
            form_data['RatebookRevisionType'] = 'Initial Draft'
            form_data['RatebookStatusType'] = 'Draft'
            form_data['RatebookChangeType'] = 'Initial'
            created = False
            if not RatebookMetadata.objects.filter(**form_data):
                form_data['CreationDateTime'] = timezone.now()
                form_data['RatebookID'] = helperfuncs.generateRatebookID()
                form_data['RatebookVersion'] = 0.0
                obj = RatebookMetadata.objects.create(**form_data)
                created = True
            if created is True:
                request.session['NewRBid'] = obj.id
                if request.POST.get('CreateFrom') == 'clone':
                    return redirect('ratemanager:cloneOptions', prodCode=request.session['TemplateFormData']['ProductCode'])
                elif request.POST.get('CreateFrom') == 'fromScratch':
                    request.session['CreatedTemplateMetadata'] = obj.id
                    return redirect('ratemanager:selectFromAllExhibitsList', id=obj.id)
                elif request.POST.get('rbID'):
                    return redirect(
                        'ratemanager:selectFromExistingRbExhibitsList',
                        id=request.POST.get('rbID')
                        )
            else:
                messages.add_message(request, messages.ERROR,
                                     RATE_MANAGER['MES_0005'])
                return redirect('.')

        else:
            messages.add_message(request, messages.ERROR,
                                 'Invalid form, Try again.')
            return render(request, 'ratemanager/ProjectIdAndDateInput.html',
                          {
                              'options': options,
                              'appLabel': appLabel,
                              'form': form,
                              'title': 'Project ID & Dates'
                          })


def deleteTemplate(request, rbID):
    '''
    Deletes all the template entries and
    also the Rb metadata entry if the status is in Initial draft
    '''
    found = RatebookMetadata.objects.filter(RatebookID=rbID)
    if found and found.first().Environment == 'Production':
        messages.add_message(request, level=messages.ERROR, message="Unable to delete the template already in Production")
        return redirect('ratemanager:template')

    RatebookTemplate.objects.filter(RatebookID=rbID).delete()
    RatebookMetadata.objects.filter(RatebookID=rbID).delete()
    if not RatebookTemplate.objects.filter(RatebookID=rbID) and \
       not RatebookMetadata.objects.filter(RatebookID=rbID):
        messages.add_message(request, level=messages.INFO, message="Successfully deleted the template.")
    else:
        messages.add_message(request, level=messages.ERROR, message="Unable to delete the template.")
    return redirect('ratemanager:template')


def moreTemplateDetailsPopup(request, RBpk):
    obj = RatebookMetadata.objects.get(pk=RBpk)
    moreSearchTableHeadersNames = [
        'Carrier', 'State', 'LineofBusiness', 'UWCompany', 'PolicyType', 'PolicySubType', 'ProductCode', 'NewBusinessEffectiveDate',  'RenewalEffectiveDate', 'NewBusinessExpiryDate', 'RenewalExpiryDate', 'CreationDateTime', 'RatebookStatusType',
        'RatebookRevisionType', 'RatebookChangeType', 'ActivationDate', 'ActivationTime',
        'MigrationDate', 'MigrationTime', 'ProjectDescription', 'Environment',
        'isDeleted', 'onHold', ]
    fieldsDict = {x.name: x for x in RatebookMetadata._meta.fields}
    moreSearchTableHeaders = [fieldsDict[field] for field in moreSearchTableHeadersNames]
    return render(request, 'ratemanager/moreDetailsSearchResults.html',
                  {'moreSearchTableHeaders': moreSearchTableHeaders,
                   'obj': obj})
