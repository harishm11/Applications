from ratemanager.forms import createTempleteForm, createRatingExhibitsFromSet
from django.shortcuts import render, redirect
import ratemanager.views.HelperFunctions as helperfuncs
from datetime import datetime
from ratemanager.models import RatebookMetadata
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import FormView
from django.contrib import messages


def createTemplate(request):
    options = helperfuncs.SIDEBAR_OPTIONS
    appLabel = 'ratemanager'

    if request.method == 'POST':
        rate_details = request.POST.copy()
        form = createTempleteForm(rate_details)
        if rate_details['CreateIntent'] == 'new':
            if form.is_valid():
                rbMeta = form.save(commit=False)
                rbMeta.RatebookRevisionType = 'Template'
                rbMeta.RatebookStatusType = 'Template'
                rbMeta.RatebookChangeType = 'Template'
                rbMeta.CreationDateTime = datetime.now()
                rbMeta.RatebookID = helperfuncs.generateRatebookID()
                rbMeta.RatebookVersion = 0.0
                rbMeta.save()
                return redirect('ratemanager:cloneOptions', pk=rbMeta.id)
                # return redirect('ratemanager:createExhibitsAndVariables', pk=rbMeta.id)
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


class createExhibitsAndVariables(SingleObjectMixin, FormView):
    """
    For adding RatingVariables to an Exhibit, or editing them.
    """

    model = RatebookMetadata
    template_name = "ratemanager/createExhibitsAndVariables.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=RatebookMetadata.objects.all())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=RatebookMetadata.objects.all())
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        """
        Use our big formset of formsets, and pass in the RatebookMetadata object.
        """
        return createRatingExhibitsFromSet(
            **self.get_form_kwargs(), instance=self.object
        )

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        form.save()

        messages.add_message(self.request, messages.SUCCESS, "Changes were saved.")

        return redirect('ratemanager:createExhibitsAndVariables', pk=self.object.id)

    def get_context_data(self, **kwargs):
        context = super(createExhibitsAndVariables, self).get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        context['options'] = helperfuncs.SIDEBAR_OPTIONS
        context['appLabel'] = 'ratemanager'
        return context
