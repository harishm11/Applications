from authenticate.models import Homepagemodel
from django.views import generic
from django.utils.decorators import method_decorator
from ..forms import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# from ..decorators import has_permission


@method_decorator(login_required, name='dispatch')
class homeview(generic.ListView):

    template_name = 'base.html'
    data = Homepagemodel.objects.all()

    def get_queryset(self):
        return Homepagemodel.objects.all()


@login_required
def switch_group(request):
    context = {}
    existing_groups = request.session.get('session_groups')

    if existing_groups:
        # Get the corresponding group objects
        existing_group_objects = Group.objects.filter(name__in=existing_groups)

        # Clear the user's existing group memberships
        request.user.groups.clear()

        # Add the groups from the session back to the user's group memberships
        request.user.groups.add(*existing_group_objects)

        # Delete the session variable
        if 'selected_group_id' in request.session and request.session['selected_group_id']:
            del request.session['selected_group_id']
    else:
        existing_groups = list(
            request.user.groups.values_list('name', flat=True))
        request.session['session_groups'] = existing_groups

    if request.method == 'POST':
        form = SwitchGroupForm(request.user, request.POST)
        if form.is_valid():
            selected_group = form.cleaned_data['group']
            # Store the selected group in the session
            request.session['selected_group_id'] = selected_group.id
            # Redirect to the home page or any other page
            return redirect('home')
    else:
        form = SwitchGroupForm(request.user)

    context['form'] = form

    return render(request, 'registration/switchrole.html', context)


def feedbackview(request):
    if request.method == "POST":
        form = feedbackpageform(request.POST)
        if form.is_valid():
            form.instance.Username = request.user
            form.save()
            return redirect('/')
    else:
        form = feedbackpageform()
    context = {
        "form": form}
    return render(request, "feedback.html", context)
