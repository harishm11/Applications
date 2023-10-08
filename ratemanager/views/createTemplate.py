from ratemanager.forms import createTempleteForm, editExhibitForm, addExhibitForm
from django.shortcuts import render, redirect
import ratemanager.views.HelperFunctions as helperfuncs
from datetime import datetime
from ratemanager.models import RatebookMetadata, RatebookTemplate
from django.contrib import messages


def createTemplate(request):
    options = helperfuncs.SIDEBAR_OPTIONS
    appLabel = 'ratemanager'

    if request.method == 'POST':
        rate_details = request.POST.copy()
        form = createTempleteForm(rate_details)
        if rate_details['CreateIntent'] == 'new':
            if form.is_valid():

                # save the Form data to session
                request.session['createTemplateFormData'] = rate_details

                # redirect to clone options view
                return redirect('ratemanager:cloneOptions', prodCode=rate_details['ProductCode'])
        if rate_details['CreateIntent'] == 'raterevision':
            ids = helperfuncs.extractIdentityDetails(rate_details)
            foundRB = RatebookMetadata.objects.all().filter(**ids).order_by('-RatebookVersion').first()
            if not foundRB:
                messages.add_message(request, messages.ERROR, "No Ratebook found with the given details")
                return redirect('ratemanager:createTemplate')
            else:
                return redirect('/ratemanager/exportRB/?selectedRBs=' + '_'.join([foundRB.RatebookID, str(foundRB.RatebookVersion), foundRB.RatebookName]))

    if request.method == 'GET':
        initial = {
            'NewBusinessEffectiveDate': datetime.today(),
            'RenewalEffectiveDate': datetime.today(),
            'ActivationDate': datetime.today(),
            'ActivationTime': datetime.now(),
            'MigrationDate': datetime.today(),
            'MigrationTime': datetime.now()
        }

        form = createTempleteForm(initial=initial)

        return render(request, 'ratemanager/createTemplate.html',
                      {
                        'form': form,
                        'options': options,
                        'appLabel': appLabel
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
    RatebookTemplate.objects.get(pk=pk).delete()
    messages.add_message(request, messages.SUCCESS, "Exhibit Deleted Successfully")
    return redirect('ratemanager:listExhibits', request.session['currentlyEditingRatebook'])
