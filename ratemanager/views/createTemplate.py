from ratemanager.forms import editExhibitForm, addExhibitForm, selectExhibitListsForm, selectExhibitListsFormExistingRB
from django.shortcuts import render, redirect
import ratemanager.views.HelperFunctions as helperfuncs
from ratemanager.models.ratebookmetadata import RatebookMetadata
from ratemanager.models.ratebooktemplate import RatebookTemplate
from ratemanager.models.ratingexhibits import RatingExhibits
from django.contrib import messages
from django.utils.html import format_html


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
        found = RatebookMetadata.objects.filter(RatebookID=id.split('_')[0])
        if found and found.first().Environment == 'Production':
            messages.add_message(request, level=messages.ERROR, message="Unable to Edit the template already in Production.")
            return redirect('ratemanager:ratebook')
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

        if form.is_valid():
            form_data = form.cleaned_data
            for i in form_data['toAddExhibits']:
                sourceExhibit = RatebookTemplate.objects.all().filter(RatebookExhibit=i).first()
                newObj, _ = RatebookTemplate.objects.get_or_create(RatebookID=id.split('_')[0], RatebookExhibit=i)
                for j in sourceExhibit.ExhibitVariables.all():
                    newObj.ExhibitVariables.add(j)
                for j in sourceExhibit.ExhibitCoverages.all():
                    newObj.ExhibitCoverages.add(j)
            for i in RatebookTemplate.objects.filter(RatebookID=id.split('_')[0]):
                if i.RatebookExhibit not in form_data['toAddExhibits']:
                    i.delete()
        return redirect('ratemanager:listExhibits', id)


def selectFromExistingRbExhibitsList(request, id):
    options = helperfuncs.SIDEBAR_OPTIONS
    appLabel = 'ratemanager'

    cloneFromRBid = request.POST.get('toCloneRB') or id
    rbID = cloneFromRBid.split('_')[0]

    if request.method == 'GET':
        form = selectExhibitListsFormExistingRB(rbID=rbID)
        newRbID = request.session['NewRBid']
        found = RatebookMetadata.objects.filter(RatebookID=newRbID.split('_')[0])
        if found and found.first().Environment == 'Production':
            messages.add_message(request, level=messages.ERROR, message="Unable to edit the template already in Production.")
            return redirect('ratemanager:ratebook')
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

        if form.is_valid():
            form_data = form.cleaned_data
            for i in form_data['toAddExhibits']:
                sourceExhibit = RatebookTemplate.objects.all().filter(
                    RatebookID=rbID.split('_')[0],
                    RatebookExhibit=i).first()
                newObj, _ = RatebookTemplate.objects.get_or_create(
                    RatebookID=newRbID.split('_')[0], RatebookExhibit=i)
                for j in sourceExhibit.ExhibitVariables.all():
                    newObj.ExhibitVariables.add(j)
                for j in sourceExhibit.ExhibitCoverages.all():
                    newObj.ExhibitCoverages.add(j)
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
                    'title': 'List Exhibits in Template',
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
    filteredExhibits = helperfuncs.fetchRatebookSpecificVersion(
        rbID=ExhibitObj.RatebookID,
        rbVersion=RatebookMetadata.objects.filter(
            RatebookID=ExhibitObj.RatebookID
            ).order_by('-RatebookVersion').first().RatebookVersion
            ).order_by('Coverage', 'Exhibit').filter(
                Exhibit=ExhibitObj.RatebookExhibit.Exhibit
                )
    if filteredExhibits:
        df = helperfuncs.convert2Df(filteredExhibits)
        idf = helperfuncs.inverseTransform(df)
        idf = idf.fillna('')
        dfHTML = format_html(idf.to_html(table_id='example', index=False))
    else:
        dfHTML = format_html("<h1>No Data Found</h1>")
    return render(request, 'ratemanager/previewExhibit.html',
                  {
                    'ExhibitObj': ExhibitObj,
                    'dfHTML': dfHTML
                    })


def resumeTemplateDraftCreation(request, id):
    return redirect('ratemanager:selectFromAllExhibitsList', id=id)
