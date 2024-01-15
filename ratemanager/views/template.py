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

    if request.method == 'POST':
        ratebook_details = request.POST.copy()
        # save the Form data to session before validation and main action
        request.session['TemplateFormData'] = ratebook_details
        form = createTemplateForm(ratebook_details)
        if form.is_valid():
            # save the cleaned Form data to session
            form_data = form.cleaned_data

            # check for existing template/Ratebook in production and if found show that it already exists.
            identityDetails = helperfuncs.extractIdentityDetails(form_data)
            searchResults = RatebookMetadata.objects.filter(
                    **identityDetails)
            if request.POST['submit'] == 'Create a new Ratebook/Template':
                return redirect('ratemanager:projectIdAndDateInput')
            if searchResults.count() > 0 or request.POST['submit'] == 'Search':

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
                                'searchResults': searchResults
                                })
        else:
            messages.add_message(request, messages.ERROR,
                                 "Form invalid, Try Again")
            return redirect('ratemanager:template')

    if request.method == 'GET':
        initial = {}
        if request.session.get('TemplateFormData'):
            createTemplateFormPrefilled = createTemplateForm(
                initial=request.session['TemplateFormData']
            )
        else:
            createTemplateFormPrefilled = createTemplateForm(initial=initial)

        return render(request, 'ratemanager/Template.html',
                      {
                          'createTemplateForm': createTemplateFormPrefilled,
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
        form = projectIdAndDateInputForm(initial=initial)
        return render(request, 'ratemanager/ProjectIdAndDateInput.html',
                      {
                          'options': options,
                          'appLabel': appLabel,
                          'form': form,
                          'title': 'Project ID & Dates'
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
            if request.POST['CreateFrom'] == 'clone':
                return redirect('ratemanager:cloneOptions', prodCode=request.session['TemplateFormData']['ProductCode'])
            elif request.POST['CreateFrom'] == 'fromScratch':
                request.session['CreatedTemplateMetadata'] = obj.id
                return redirect('ratemanager:selectFromAllExhibitsList', id=obj.id)

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
    options = helperfuncs.SIDEBAR_OPTIONS
    appLabel = 'ratemanager'

    RatebookTemplate.objects.all().filter(RatebookID=rbID).delete()
    RatebookMetadata.objects.filter(
        RatebookID=rbID,
        RatebookStatusType='Initial Draft'
        ).delete()
    messages.add_message(request, level=messages.INFO, message="Successfully deleted the template.")
    initial = {}
    if request.session.get('TemplateFormData'):
        createTemplateFormPrefilled = createTemplateForm(
            initial=request.session['TemplateFormData']
            )
    else:
        createTemplateFormPrefilled = createTemplateForm(initial=initial)

    return render(request, 'ratemanager/Template.html',
                  {
                    'createTemplateForm': createTemplateFormPrefilled,
                    'options': options,
                    'appLabel': appLabel,
                    'title': 'Template',
                    })
