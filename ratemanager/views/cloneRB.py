from django.shortcuts import render, redirect
from ratemanager.models import RatebookMetadata, RatebookTemplate
from ratemanager.views import HelperFunctions as helperfuncs
from django.utils import timezone
from ratemanager.forms import createTempleteForm
from django.contrib import messages


def cloneOptions(request, prodCode):
    '''
    This view displays the options for cloning a ratebook.  The user can choose to clone the ratebook form the same product code only.
    '''
    options = helperfuncs.SIDEBAR_OPTIONS
    appLabel = 'ratemanager'

    request.session['ProductCode'] = prodCode
    similarRBs = RatebookMetadata.objects.filter(ProductCode_id=prodCode).exclude(RatebookStatusType__in=["Template", "Cloned Template"]).order_by('ProductCode')
    if similarRBs and request.method == 'GET':
        return render(request, 'ratemanager/cloneOptions.html',
                      context={
                            'options': options,
                            'appLabel': appLabel,
                            'similarRBs': similarRBs,
                            'prodCode': prodCode,
                            'title': 'Clone Template'
                        })
    # for POST request and no similar ratebooks found
    # fetch the form data from session
    formdata = request.session.get('createTemplateFormData')
    form = createTempleteForm(formdata)
    rbMeta = form.save(commit=False)

    # set the fields that are not in the form
    rbMeta.RatebookRevisionType = 'Template'
    rbMeta.RatebookStatusType = 'Template'
    rbMeta.RatebookChangeType = 'Template'
    rbMeta.CreationDateTime = timezone.now()
    rbMeta.RatebookID = helperfuncs.generateRatebookID()
    rbMeta.RatebookVersion = 0.0
    rbMeta.save()
    return redirect('ratemanager:listExhibits', pk=rbMeta.id)


def cloneRB(request):
    '''
    This view clones the ratebook and all of its associated exhibits and variables.
    '''
    tocloneExhibitlist = request.POST.getlist('toAddExhibits')

    rbID = request.POST.get('rbID')
    # create RatebookMetadata object from the saved createTemplateFormData
    createTemplateFormData = request.session.get('createTemplateFormData')
    formObj = createTempleteForm(createTemplateFormData)
    rb = formObj.save(commit=False)
    rb.RatebookRevisionType = 'Cloned Template'
    rb.RatebookStatusType = 'Cloned Template'
    rb.RatebookChangeType = 'Cloned Template'
    rb.CreationDateTime = timezone.now()
    rb.RatebookID = helperfuncs.generateRatebookID()
    rb.RatebookVersion = 0.0
    rb.save()
    ExhibitObjs = RatebookTemplate.objects.filter(RatebookID=rbID, id__in=tocloneExhibitlist)
    for i in ExhibitObjs:
        clonedExhibit = RatebookTemplate()
        # set attributes of cloned exhibit to the attributes of the original exhibit
        for field in i._meta.fields:
            # does not work for many to many fields so need to handle them separately
            setattr(clonedExhibit, field.name, getattr(i, field.name))
        clonedExhibit.pk = None
        clonedExhibit.RatebookID = rb.RatebookID
        clonedExhibit.save()
        # find all many to many fields
        many_to_many_fields = [field for field in RatebookTemplate._meta.get_fields() if field.many_to_many]
        for field in many_to_many_fields:
            for row in getattr(i, field.name).all():
                getattr(clonedExhibit, field.name).add(row)
        # set the id to None so that it is saved as a new record and set the newly generated ratebook ID and save
    messages.add_message(request, messages.INFO, "Cloned Successful with New ID" + rb.RatebookID)
    return redirect('ratemanager:listExhibits', pk=rb.id)
