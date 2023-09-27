# create a view to clone a ratebook metadata object with related objects also cloned

from django.shortcuts import render, redirect
from django.contrib import messages
from ratemanager.models import RatebookMetadata, RatingExhibits, RatingVariables
from ratemanager.views import HelperFunctions as helperfuncs


def cloneOptions(request, pk):
    options = helperfuncs.SIDEBAR_OPTIONS
    appLabel = 'ratemanager'

    rb = RatebookMetadata.objects.get(pk=pk)
    similarRBs = RatebookMetadata.objects.filter(ProductCode_id=rb.ProductCode_id)

    return render(request, 'ratemanager/cloneOptions.html', locals())


def clone_ratebook(request, ratebook_id):
    # Get the RatebookMetadata object to be cloned
    ratebook = RatebookMetadata.objects.get(id=ratebook_id)

    # Create a new RatebookMetadata object with the same attributes as the original
    new_ratebook = RatebookMetadata.objects.create(
        name=ratebook.name + ' (Clone)',
        description=ratebook.description,
        effective_date=ratebook.effective_date,
        expiration_date=ratebook.expiration_date,
        status=ratebook.status,
        created_by=request.user,
        modified_by=request.user
    )

    # Clone all related RatingExhibits objects
    for exhibit in ratebook.rating_exhibits.all():
        RatingExhibits.objects.create(
            ratebook=new_ratebook,
            name=exhibit.name,
            description=exhibit.description,
            order=exhibit.order,
            created_by=request.user,
            modified_by=request.user
        )

    # Clone all related RatingVariables objects
    for variable in ratebook.rating_variables.all():
        RatingVariables.objects.create(
            ratebook=new_ratebook,
            name=variable.name,
            description=variable.description,
            order=variable.order,
            created_by=request.user,
            modified_by=request.user
        )

    # Redirect to the cloned RatebookMetadata object's detail view
    messages.success(request, 'Ratebook cloned successfully.')
    return redirect('ratebook_detail', ratebook_id=new_ratebook.id)
