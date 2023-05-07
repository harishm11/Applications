from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from ..forms import *
from django.utils.decorators import method_decorator
from django.views import generic

from authenticate.models import Homepagemodel


@method_decorator(login_required, name='dispatch')
class homeview(generic.ListView):
    template_name = 'base.html'
    data = Homepagemodel.objects.all()

    def get_queryset(self):
        return Homepagemodel.objects.all()


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
