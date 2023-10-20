from ratemanager.forms import createTempleteForm, mainActionForm, projectIdAndDateInputForm
from django.shortcuts import render, redirect
import ratemanager.views.HelperFunctions as helperfuncs
from ratemanager.models import RatebookMetadata
from django.contrib import messages
from django.utils import timezone


def template(request):
    options = helperfuncs.SIDEBAR_OPTIONS
    appLabel = 'ratemanager'

    if request.method == 'POST':
        ratebook_details = request.POST.copy()
        # save the Form data to session before validation and main action
        request.session['TemplateFormData'] = ratebook_details
        form = createTempleteForm(ratebook_details)
        if ratebook_details['MainAction'] == 'new':
            if form.is_valid():
                # save the cleaned Form data to session
                form_data = form.cleaned_data

                # check for existing template/Ratebook in production and if found show that it already exists.
                identityDetails = helperfuncs.extractIdentityDetails(form_data)
                searchResults = RatebookMetadata.objects.filter(**identityDetails)
                if searchResults.count() > 0:
                    # check for matching drafts if found show the draft.
                    if searchResults.filter(RatebookStatusType='Initial Draft').count() > 0:
                        messages.add_message(request, messages.INFO, 'Found an existing draft for the given ratebook details.')
                    else:
                        messages.add_message(request, messages.INFO, 'Another Ratebook with same details already exists.')

                    searchResults.order_by(
                        'RatebookID', 'RatebookStatusType', '-RatebookVersion'
                        ).distinct('RatebookID', 'RatebookStatusType')

                    return render(request, 'ratemanager/Template.html',
                                  {
                                    'createTempleteForm': form,
                                    'options': options,
                                    'appLabel': appLabel,
                                    'mainActionForm': mainActionForm(initial={'MainAction': ratebook_details['MainAction']}),
                                    'title': 'Template',
                                    'searchResults': searchResults
                                    })
                else:
                    return redirect('ratemanager:projectIdAndDateInput')

        else:
            messages.add_message(request, messages.ERROR, "Form invalid, Try Again")
            return redirect('ratemanager:template')

    if request.method == 'GET':
        initial = {}
        if request.session.get('TemplateFormData'):
            createTempleteFormPrefilled = createTempleteForm(
                initial=request.session['TemplateFormData']
                )
        else:
            createTempleteFormPrefilled = createTempleteForm(initial=initial)

        return render(request, 'ratemanager/Template.html',
                      {
                        'createTempleteForm': createTempleteFormPrefilled,
                        'options': options,
                        'appLabel': appLabel,
                        'mainActionForm': mainActionForm(initial={'MainAction': 'view'}),
                        'title': 'Template',
                        })


def projectIdAndDateInput(request):

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
                        'form': form,
                        })

    if request.method == 'POST':
        form = projectIdAndDateInputForm(request.POST)
        if form.is_valid():
            # check for valid Project ID
            form_data = form.cleaned_data
            form_data['ProjectID'] = form_data['ProjectID'].strip()
            if RatebookMetadata.objects.filter(ProjectID=form_data['ProjectID']).count() > 0:
                messages.add_message(request, messages.ERROR, 'ProjectID already exists, use different one.')
                return render(request, 'ratemanager/ProjectIdAndDateInput.html',
                              {
                                'form': form,
                                })
            # save the forms data to RB metadatatable
            searchOptions = createTempleteForm(data=request.session['TemplateFormData'])
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

            if request.POST['CreateFrom'] == 'clone':
                return redirect('ratemanager:cloneOptions', prodCode=request.session['TemplateFormData']['ProductCode'])
            elif request.POST['CreateFrom'] == 'fromScratch':
                request.session['CreatedTemplateMetadata'] = obj.id
                return redirect('/ratemanager/selectExhibitOptions/?showAllExhibits=True')

        else:
            messages.add_message(request, messages.ERROR, 'Invalid form, Try again.')
            return render(request, 'ratemanager/ProjectIdAndDateInput.html',
                          {
                            'form': form,
                            })
