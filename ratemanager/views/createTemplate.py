from ratemanager.forms import editExhibitForm, addExhibitForm, selectExhibitListsForm, selectExhibitListsFormExistingRB
from django.shortcuts import render, redirect
import ratemanager.views.HelperFunctions as helperfuncs
from ratemanager.models import RatebookMetadata, RatebookTemplate, RatingExhibits
from django.contrib import messages


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


def selectFromAllExhibitsList(request, id):
    options = helperfuncs.SIDEBAR_OPTIONS
    appLabel = 'ratemanager'

    if request.method == 'GET':
        form = selectExhibitListsForm()
        choices = RatingExhibits.objects.all()
        form.fields['toAddExhibits'].queryset = choices
        initial = RatingExhibits.objects.filter(ratebooktemplate__in=RatebookTemplate.objects.filter(RatebookID=id.split('_')[0]))
        form.fields['toAddExhibits'].initial = initial

        return render(request, 'ratemanager/selectExhibitsOptions.html',
                      {
                            'form': form,
                            'options': options,
                            'appLabel': appLabel,
                            'title': 'Add Exhibits',
                            'id': id
                        })

    if request.method == 'POST':
        form = selectExhibitListsForm(request.POST)
        choices = RatingExhibits.objects.all()
        form.fields['toAddExhibits'].queryset = choices
        initial = RatingExhibits.objects.filter(ratebooktemplate__in=RatebookTemplate.objects.filter(RatebookID=id.split('_')[0]))
        form.fields['toAddExhibits'].initial = initial

        print(form)
        if form.is_valid():
            form_data = form.cleaned_data
            for i in form_data['toAddExhibits']:
                newObj, _ = RatebookTemplate.objects.get_or_create(RatebookID=id.split('_')[0], RatebookExhibit=i)
                sourceExhibit = RatebookTemplate.objects.all().filter(RatebookExhibit=i).first()
                for i in sourceExhibit.ExhibitVariables.all():
                    newObj.ExhibitVariables.add(i)
                for i in sourceExhibit.ExhibitCoverages.all():
                    newObj.ExhibitCoverages.add(i)
        return redirect('ratemanager:listExhibits', id)


def selectFromExistingRbExhibitsList(request, id):
    options = helperfuncs.SIDEBAR_OPTIONS
    appLabel = 'ratemanager'

    cloneFromRBid = request.POST.get('toCloneRB') or id
    rbID = cloneFromRBid.split('_')[0]

    if request.method == 'GET':
        form = selectExhibitListsFormExistingRB(rbID=rbID)
        newRbID = request.session['NewRBid']
        initial = RatingExhibits.objects.filter(ratebooktemplate__in=RatebookTemplate.objects.filter(RatebookID=newRbID))
        form.fields['toAddExhibits'].initial = initial
        return render(request, 'ratemanager/selectExhibitsOptions.html',
                      {
                            'form': form,
                            'options': options,
                            'appLabel': appLabel,
                            'title': 'Add Exhibits'
                        })

    if request.method == 'POST':
        newRbID = request.session['NewRBid']
        form = selectExhibitListsFormExistingRB(data=request.POST, rbID=rbID)

        print(form)
        if form.is_valid():
            form_data = form.cleaned_data
            for i in form_data['toAddExhibits']:
                newObj, _ = RatebookTemplate.objects.get_or_create(RatebookID=newRbID.split('_')[0], RatebookExhibit=i)
                sourceExhibit = RatebookTemplate.objects.all().filter(RatebookExhibit=i).first()
                for i in sourceExhibit.ExhibitVariables.all():
                    newObj.ExhibitVariables.add(i)
                for i in sourceExhibit.ExhibitCoverages.all():
                    newObj.ExhibitCoverages.add(i)
            return redirect('ratemanager:selectFromAllExhibitsList', newRbID)
        else:
            messages.add_message(request, messages.SUCCESS, form.errors)
            return redirect('ratemanager:selectFromExistingRbExhibitsList', cloneFromRBid)


def listExhibits(request, pk):
    options = helperfuncs.SIDEBAR_OPTIONS
    appLabel = 'ratemanager'

    rbid, rbver = pk.split('_')
    ExhibitObjs = RatebookTemplate.objects.filter(RatebookID=rbid)
    request.session['currentlyEditingRatebook'] = pk

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
    # delete the exhibit-rbid relationship from RatebookTemplate table
    RatebookTemplate.objects.get(pk=pk).delete()
    messages.add_message(request, messages.SUCCESS, "Exhibit Deleted Successfully")
    return redirect('ratemanager:listExhibits', request.session['currentlyEditingRatebook'])


def previewExhibit(request, Exhibit_id):
    ExhibitObj = RatebookTemplate.objects.get(pk=Exhibit_id)

    return render(request, 'ratemanager/previewExhibit.html',
                  {
                    'ExhibitObj': ExhibitObj,
                    })


def resumeTemplateDraftCreation(request, id):
    return redirect('ratemanager:selectFromAllExhibitsList', id=id)
