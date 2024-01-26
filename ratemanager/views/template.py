from ratemanager.forms import createTemplateForm, projectIdAndDateInputForm
from django.shortcuts import render, redirect
import ratemanager.views.HelperFunctions as helperfuncs
from ratemanager.models.ratebookmetadata import RatebookMetadata
from ratemanager.models.ratebooktemplate import RatebookTemplate

from django.contrib import messages
from django.utils import timezone
from myproj.messages import RATE_MANAGER


def template(request):
    options = helperfuncs.SIDEBAR_OPTIONS
    appLabel = 'ratemanager'

    # Left overs 'id', 'Environment', 'isDeleted', 'onHold', 'retrofitReq', 'Carrier', 'State', 'LineofBusiness', 'UWCompany', 'PolicyType', 'PolicySubType', 'ProductCode', 'NewBusinessExpiryDate', 'RenewalExpiryDate',
    searchResultTableHeadersNamesOrder = ['RatebookName', 'RatebookID',  'ProjectID', 'ProjectDescription', 'RatebookVersion', 'RatebookRevisionType', 'RatebookStatusType', 'RatebookChangeType', 'NewBusinessEffectiveDate',  'RenewalEffectiveDate',  'ActivationDate', 'ActivationTime', 'MigrationDate', 'MigrationTime', 'CreationDateTime']
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
                **identityDetails)
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
                        'searchResultTableHeaders': searchResultTableHeaders
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
                data=request.session['TemplateFormData'])
        if searchOptions.is_valid():
            searchOptionsData = searchOptions.cleaned_data
        return render(request, 'ratemanager/ProjectIdAndDateInput.html',
                      {
                          'options': options,
                          'appLabel': appLabel,
                          'form': form,
                          'title': 'Project ID & Dates',
                          'searchOptionsData': searchOptionsData,
                          'rbID': rbID
                      })

    if request.method == 'POST':
        form = projectIdAndDateInputForm(request.POST)
        if form.is_valid():
            # check for valid Project ID
            form_data = form.cleaned_data
            form_data['ProjectID'] = form_data['ProjectID'].strip()
            if not form_data['ProjectID']:
                messages.add_message(
                    request, messages.ERROR, 'Please assign a valid Project ID.')
                return render(request, 'ratemanager/ProjectIdAndDateInput.html',
                              {
                                  'options': options,
                                  'appLabel': appLabel,
                                  'form': form,
                                  'title': 'Project ID & Dates'
                              })
            if RatebookMetadata.objects.filter(ProjectID=form_data['ProjectID']).count() > 0:
                messages.add_message(
                    request, messages.ERROR, 'ProjectID already exists, use different one.')
                return render(request, 'ratemanager/ProjectIdAndDateInput.html',
                              {
                                  'options': options,
                                  'appLabel': appLabel,
                                  'form': form,
                                  'title': 'Project ID & Dates'
                              })
            # save the forms data to RB meta data table
            searchOptions = createTemplateForm(
                data=request.session['TemplateFormData'])
            searchOptions.is_valid()
            form_data.update(
                searchOptions.cleaned_data
            )
            form_data['RatebookRevisionType'] = 'Initial Draft'
            form_data['RatebookStatusType'] = 'Initial Draft'
            form_data['RatebookChangeType'] = 'Initial Draft'
            form_data['CreationDateTime'] = timezone.now()
            form_data['RatebookID'] = helperfuncs.generateRatebookID()
            form_data['RatebookVersion'] = 0.0
            obj = RatebookMetadata.objects.create(**form_data)
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

    RatebookTemplate.objects.all().filter(RatebookID=rbID).delete()
    RatebookMetadata.objects.filter(
        RatebookID=rbID,
        RatebookStatusType='Initial Draft'
        ).delete()
    messages.add_message(request, level=messages.INFO, message="Successfully deleted the template.")

    return redirect('ratemanager:template')
