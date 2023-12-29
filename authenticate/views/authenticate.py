from django.contrib.auth import login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.views import *
from myproj.utils import handleformerror

def login_view(request):
    context = {}
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # request.session['selected_group_id'] = 1
            return redirect('/')
        else:
            context['message'] = handleformerror(form)
    else:
        form = AuthenticationForm(request)
    context['form'] = form
    return render(request, "registration/login.html", context)


def logout_view(request):
    existing_groups = request.session.get('session_groups')
    if request.method == "POST":

        if existing_groups:
            # Get the corresponding group objects
            existing_group_objects = Group.objects.filter(
                name__in=existing_groups)

            # Clear the user's existing group memberships
            request.user.groups.clear()

            # Add the groups from the session back to the user's group memberships
            request.user.groups.add(*existing_group_objects)

        logout(request)
        return redirect("/login/")
    return render(request, "registration/logout.html", {})


class PasswordResetByUser(PasswordChangeView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = '/'


def register_view(request):
    context = {}
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/login')
    else:
        context['message'] = handleformerror(form)
    context['form'] = form
    return render(request, "registration/register.html", context)


