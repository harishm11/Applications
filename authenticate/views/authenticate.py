from django.contrib.auth import login, logout

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.views import *


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = AuthenticationForm(request)
    context = {
        "form": form}
    return render(request, "registration/login.html", context)


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("/login/")
    return render(request, "registration/logout.html", {})


class PasswordResetByUser(PasswordChangeView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = '/'


def register_view(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/login')
    context = {"form": form}
    return render(request, "registration/register.html", context)
