from ratemanager.forms import createTempleteForm, editExhibitForm, addExhibitForm, selectExhibitListsForm, mainActionForm
from django.shortcuts import render, redirect
import ratemanager.views.HelperFunctions as helperfuncs
from datetime import datetime
from django.utils import timezone
from ratemanager.models import RatebookMetadata, RatebookTemplate, RatingExhibits
from django.contrib import messages


def createTemplate(request):
    options = helperfuncs.SIDEBAR_OPTIONS
    appLabel = 'ratemanager'

    if request.method == 'POST':
        rate_details = request.POST.copy()
        form = createTempleteForm(rate_details)
        if rate_details['MainAction'] == 'new':
            if form.is_valid():

                # save the Form data to session
                request.session['createTemplateFormData'] = rate_details

                # check for matching drafts if found show the draft.

                # check for existing template/Ratebook in production and if found show that it already exists.

                # redirect to clone options view
                return redirect('ratemanager:cloneOptions', prodCode=rate_details['ProductCode'])
        elif rate_details['MainAction'] == 'raterevision':
            ids = helperfuncs.extractIdentityDetails(rate_details)
            foundRB = RatebookMetadata.objects.all().filter(**ids).order_by('-RatebookVersion').first()
            if not foundRB:
                messages.add_message(request, messages.ERROR, "No Ratebook found with the given details")
                return redirect('ratemanager:createTemplate')
            else:
                return redirect('/ratemanager/exportRB/?selectedRBs=' + '_'.join([foundRB.RatebookID, str(foundRB.RatebookVersion), foundRB.RatebookName]))
        else:
            messages.add_message(request, messages.ERROR, "Invalid Create Intent Selection, Try Again")
            return redirect('ratemanager:createTemplate')

    if request.method == 'GET':
        initial = {
            'NewBusinessEffectiveDate': datetime.today(),
            'RenewalEffectiveDate': datetime.today(),
            'ActivationDate': datetime.today(),
            'ActivationTime': timezone.now(),
            'MigrationDate': datetime.today(),
            'MigrationTime': timezone.now()
        }
        if request.session['createTemplateFormData']:
            createTempleteFormPrefilled = createTempleteForm(
                initial=request.session['createTemplateFormData']
                )
        else:
            createTempleteFormPrefilled = createTempleteForm(initial=initial)
        similarRBs = RatebookMetadata.objects.filter().exclude(RatebookStatusType__in=["Template", "Cloned Template"]).order_by('RatebookID').distinct('RatebookID')
        return render(request, 'ratemanager/createTemplate.html',
                      {
                        'createTempleteForm': createTempleteFormPrefilled,
                        'options': options,
                        'appLabel': appLabel,
                        'mainActionForm': mainActionForm(initial={'MainAction': 'view'}),
                        'title': 'Create Template',
                        'similarRBs': similarRBs
                        })


def editExhibitTemplate(request, pk):
    options = helperfuncs.SIDEBAR_OPTIONS
    appLabel = 'ratemanager'

    if request.method == 'GET':
        # send filled form with data of the exhibit
        exhibit = RatebookTemplate.objects.get(pk=pk)
        form = editExhibitForm(instance=exhibit)
        form.fields['RatebookExhibit'].disabled = True
        return render(request, 'ratemanager/editExhibitTemplate.html',
                      {
                        'form': form,
                        'options': options,
                        'appLabel': appLabel,
                        'exhibit': exhibit,
                        'pk': pk,
                        })
    if request.method == 'POST':
        form = editExhibitForm(request.POST, instance=RatebookTemplate.objects.get(pk=pk))
        form.fields['RatebookExhibit'].disabled = True
        if form.is_valid():
            instance = form.save(commit=False)
            # modify instance if needed
            instance.save()
            form.save_m2m()
            messages.add_message(request, messages.SUCCESS, "Exhibit Saved Successfully")
        return redirect('ratemanager:listExhibits', request.session['currentlyEditingRatebook'])


def addExhibit2Template(request):
    options = helperfuncs.SIDEBAR_OPTIONS
    appLabel = 'ratemanager'

    if request.method == 'GET':
        form = editExhibitForm()
        addForm = addExhibitForm()
        addForm.fields['Exhibit'].required = False
        form.fields['RatebookExhibit'].required = False
        return render(request, 'ratemanager/addExhibitTemplate.html',
                      {
                            'form': form,
                            'options': options,
                            'appLabel': appLabel,
                            'addExhibitForm': addForm,
                        })
    if request.method == 'POST':
        # save the Form
        exhibit_details = request.POST.copy()
        form = editExhibitForm(exhibit_details)
        addForm = addExhibitForm(exhibit_details)
        addForm.fields['Exhibit'].required = False
        form.fields['RatebookExhibit'].required = False
        if form.is_valid() and form.cleaned_data['RatebookExhibit'] is not None:
            exhibit = form.save(commit=False)
            exhibit.RatebookID = request.session['currentlyEditingRatebook'].split('_')[0]
            # modify instance if needed
            exhibit.save()
            form.save_m2m()
            messages.add_message(request, messages.SUCCESS, "Exhibit Saved Successfully")
            return redirect('ratemanager:listExhibits', request.session['currentlyEditingRatebook'])
        elif addForm.is_valid():
            Exhibit_id = addForm.save()
            form.RatebookExhibit = Exhibit_id
            exhibit = form.save(commit=False)
            exhibit.RatebookExhibit = Exhibit_id
            exhibit.RatebookID = request.session['currentlyEditingRatebook'].split('_')[0]
            # modify instance if needed
            exhibit.save()
            form.save_m2m()
            messages.add_message(request, messages.SUCCESS, "Exhibit Saved Successfully")
            return redirect('ratemanager:listExhibits', request.session['currentlyEditingRatebook'])
        else:
            messages.add_message(request, messages.ERROR, "Invalid Form Data")
            return render(request, 'ratemanager/addExhibitTemplate.html',
                          {
                            'form': form,
                            'options': options,
                            'appLabel': appLabel,
                            'addExhibitForm': addForm,
                            })


def selectExhibitList(request):
    options = helperfuncs.SIDEBAR_OPTIONS
    appLabel = 'ratemanager'
    rbid = rbID = None
    showAllExhibits = request.GET.get('showAllExhibits')
    form = selectExhibitListsForm()

    if not showAllExhibits:
        rbid = request.POST.get('toCloneRB')
        rbID = rbid.split('_')[0]

        # if no ratebook is selected redirect to clone options view with error message
        if rbid is None:
            list(messages.get_messages(request))
            messages.add_message(request, messages.ERROR, "Please select a ratebook to clone")
            return redirect(
                'ratemanager:cloneOptions',
                prodCode=request.session.get('ProductCode')
                )
        choices = RatebookTemplate.objects.all().filter(RatebookID=rbID)
        form.fields['toAddExhibits'].choices = [(choice.id, choice.RatebookExhibit) for choice in choices]
    else:
        choices = RatingExhibits.objects.all()
        form.fields['toAddExhibits'].choices = [(choice.id, choice.Exhibit) for choice in choices]

    return render(request, 'ratemanager/selectExhibitsOptions.html',
                  {
                        'form': form,
                        'options': options,
                        'appLabel': appLabel,
                        'title': 'Add Exhibits'
                    })


def listExhibits(request, pk):
    options = helperfuncs.SIDEBAR_OPTIONS
    appLabel = 'ratemanager'

    rbid, rbver = pk.split('_')
    ExhibitObjs = RatebookTemplate.objects.filter(RatebookID=rbid)
    request.session['currentlyEditingRatebook'] = pk
    if request.method == 'GET':
        return render(request, 'ratemanager/listExhibits.html',
                      {
                        'options': options,
                        'appLabel': appLabel,
                        'ExhibitObjs': ExhibitObjs,
                        'rbid': rbid,
                        'rbver': rbver,
                        'rbname': RatebookMetadata.objects.get(RatebookID=rbid, RatebookVersion=rbver).RatebookName,
                        })


def deleteExhibitTemplate(request, pk):
    # delete the exhibit-rbid relationship from ratebooktemplate table
    RatebookTemplate.objects.get(pk=pk).delete()
    messages.add_message(request, messages.SUCCESS, "Exhibit Deleted Successfully")
    return redirect('ratemanager:listExhibits', request.session['currentlyEditingRatebook'])


def previewExhibit(request, Exhibit_id):
    ExhibitObj = RatebookTemplate.objects.get(pk=Exhibit_id)

    return render(request, 'ratemanager/previewExhibit.html',
                  {
                    'ExhibitObj': ExhibitObj,
                    })
