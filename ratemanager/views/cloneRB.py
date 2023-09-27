from django.shortcuts import render, redirect
from ratemanager.models import RatebookMetadata
from ratemanager.views import HelperFunctions as helperfuncs
from datetime import datetime
from ratemanager.forms import createTempleteForm


def cloneOptions(request, prodCode):
    '''
    This view displays the options for cloning a ratebook.  The user can choose to clone the ratebook form the same product code only.
    '''
    options = helperfuncs.SIDEBAR_OPTIONS
    appLabel = 'ratemanager'

    similarRBs = RatebookMetadata.objects.filter(ProductCode_id=prodCode).exclude(RatebookStatusType="Template").order_by('ProductCode')

    return render(request, 'ratemanager/cloneOptions.html', locals())


def cloneRB(request):
    '''
    This view clones the ratebook and all of its associated exhibits and variables.
    '''
    rbid = request.POST.get('toCloneRB')
    rb = RatebookMetadata.objects.get(pk=rbid)
    createTemplateFormData = request.session.get('createTemplateFormData')
    formObj = createTempleteForm(createTemplateFormData)
    attrs = {k: v for k, v in formObj.save(commit=False).__dict__.items() if v is not None}
    clonedRB = helperfuncs.clone_object(rb, attrs)
    clonedRB.RatebookRevisionType = 'Cloned Template'
    clonedRB.RatebookStatusType = 'Cloned Template'
    clonedRB.RatebookChangeType = 'Cloned Template'
    clonedRB.CreationDateTime = datetime.now()
    clonedRB.RatebookID = helperfuncs.generateRatebookID()
    clonedRB.RatebookVersion = 0.0
    clonedRB.save()
    return redirect('ratemanager:createExhibitsAndVariables', pk=clonedRB.id)
