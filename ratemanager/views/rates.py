from django.shortcuts import redirect, render
from ratemanager.models.comments import Notes
from ratemanager.models.ratebookmetadata import EnvironmentHierarchy, RatebookMetadata
from django.contrib import messages
import ratemanager.views.HelperFunctions as helperfuncs
from ratemanager.forms import ratesReviewForm, ratesUploadForm
import pandas as pd
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import permission_required


def saveNote(request, pk):
    form = ratesReviewForm(data=request.POST)
    if form.is_valid:
        noteObj = form.save(commit=False)
        noteObj.User = request.user
        noteObj.Ratebook = RatebookMetadata.objects.get(pk=pk)
        noteObj.Category = 'Review'
        noteObj.CreationDateTime = timezone.now()
        noteObj.save()


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


@permission_required('ratemanager.SearchRateBook', raise_exception=True)
def ratebook(request):
    options = helperfuncs.SIDEBAR_OPTIONS
    appLabel = 'ratemanager'
    title = 'Rates - Rate books'

    context = helperfuncs.searchCriteriaProcessor(request)

    if request.POST.get('submit') == "Create a new Ratebook":
        return redirect('ratemanager:projectIdAndDateInput')
    if context.get('searchResults') is not None:
        page_number = request.GET.get('page') or 1
        paginator = Paginator(context.get('searchResults'), 10)
        try:
            searchResults = paginator.get_page(page_number)
        except PageNotAnInteger:
            searchResults = paginator.page(1)
        except EmptyPage:
            searchResults = paginator.page(paginator.num_pages)
    else:
        searchResults = None
    context.update({
        'options': options,
        'appLabel': appLabel,
        'title': title,
        'searchResults': searchResults
        })
    return render(request, 'ratemanager/rates/rateBooks.html', context)


@permission_required('ratemanager.Upload', raise_exception=True)
def upload(request):
    options = helperfuncs.SIDEBAR_OPTIONS
    appLabel = 'ratemanager'
    title = 'Rates-Upload'

    if request.method == 'POST':
        # Upload file to server
        uploadedFilePath = helperfuncs.uploadFile(request)
        messages.add_message(request, messages.SUCCESS, uploadedFilePath.split('/')[-1] + ' was Successfully uploaded.')
        # read the file using pandas
        df = pd.read_excel(uploadedFilePath, sheet_name=None, header=None)
        # Extract the details from the details page to identify the Ratebook
        extractedRBDetails = helperfuncs.extractRatebookDetails(df)['details_df']
        # Run some validation logic
        validated = helperfuncs.validateUpload(extractedRBDetails)

        # if validated then proceed to transform and load the data

        if not validated:
            messages.add_message(
                request, messages.ERROR, 'ValidationError:'
            )
            return redirect('.')

        # Transform the data.
        df, errors = helperfuncs.transformRBTemplate(rbID=extractedRBDetails['RatebookID'], xl_url=uploadedFilePath)
        messages.add_message(request, messages.INFO, errors)

        # Fetch the Metadata Record
        currentRbMetaObj = RatebookMetadata.objects.get(
            RatebookVersion=extractedRBDetails['RatebookVersion'],
            RatebookID=extractedRBDetails['RatebookID']
        )

        # Set additional columns required for the Table
        df['Ratebook_id'] = currentRbMetaObj.pk
        df['RatebookVersion'] = currentRbMetaObj.RatebookVersion
        df['RatebookID'] = currentRbMetaObj.RatebookID
        df['RecordStatus'] = 'Active'
        rbMetaObjDict = currentRbMetaObj.__dict__
        for key in rbMetaObjDict:
            if 'Date' in key or 'Time' in key:
                df[key] = rbMetaObjDict[key]

        helperfuncs.loadtoRatingFactors(df)
        saveNote(request, pk=currentRbMetaObj.pk)
        messages.add_message(
            request,
            messages.SUCCESS,
            'Successfully Uploaded the Rates')

    return render(request, 'ratemanager/rates/upload.html',
                  {
                      'options': options,
                      'appLabel': appLabel,
                      'title': title,
                      'ratesUploadForm': ratesUploadForm(),
                      'ratesReviewForm': ratesReviewForm()
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


@permission_required('ratemanager.Approver', raise_exception=True)
def review(request):
    options = helperfuncs.SIDEBAR_OPTIONS
    appLabel = 'ratemanager'
    title = 'Rates-Review'

    context = helperfuncs.searchCriteriaProcessor(request)
    searchResults = context.get('searchResults')
    searchResults = searchResults.exclude(Environment='Production') if searchResults is not None else None
    context.update({
        'options': options,
        'appLabel': appLabel,
        'title': title,
        'searchResults': searchResults
        })
    return render(request, 'ratemanager/rates/review.html', context)


@permission_required('ratemanager.Approver', raise_exception=True)
def reviewAndHistory(request, pk):
    obj = RatebookMetadata.objects.get(pk=pk)
    if request.method == 'GET':
        form = ratesReviewForm()
    else:
        saveNote(request, pk=obj.pk)
        obj.RatebookStatusType = request.POST.get('submit')
        obj.Environment = request.POST.get('submit')
        obj.save()
        messages.add_message(
            request=request,
            message='Successfully Changed Status.',
            level=messages.SUCCESS)
        form = ratesReviewForm()
    currentEnvironment = EnvironmentHierarchy.objects.filter(Environment=obj.RatebookStatusType).first()
    previousEnv = EnvironmentHierarchy.objects.filter(Hierarchy=currentEnvironment.Hierarchy-1).first()
    nextEnv = EnvironmentHierarchy.objects.filter(Hierarchy=currentEnvironment.Hierarchy+1).first()
    searchResultTableHeadersNamesOrder = ['CreationDateTime', 'User', 'Note']
    fieldsDict = {x.name: x for x in Notes._meta.fields}
    searchResultTableHeaders = [fieldsDict[field] for field in searchResultTableHeadersNamesOrder]
    context = {
        'form': form,
        'currentRbStatus': obj.RatebookStatusType,
        'searchResults': Notes.objects.filter(Ratebook=pk).order_by('-CreationDateTime'),
        'searchResultTableHeaders': searchResultTableHeaders,
        'previousEnv': previousEnv,
        'nextEnv': nextEnv
    }
    return render(request, 'ratemanager/rates/reviewAndHistory.html', context)


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
