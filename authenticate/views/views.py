from authenticate.models import Homepagemodel
from django.views import generic
from django.utils.decorators import method_decorator
from ..forms import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# from ..decorators import has_permission


@method_decorator(login_required, name='dispatch')
class homeview(generic.ListView):
    from django.contrib.auth.models import User

    template_name = 'base.html'
    data = Homepagemodel.objects.all()

    def get_queryset(self):
        return Homepagemodel.objects.all()


# @has_permission('Approve')
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
