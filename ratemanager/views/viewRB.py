from django.db.models import Q
from django.shortcuts import render
from ratemanager.models import Ratebooks, AllExhibits
from ratemanager.forms import ViewRBForm, SelectExhibitForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def viewRB(request):
    options = ['createRB', 'viewRB']
    appLabel = 'ratemanager'
    fields = [f.name for f in Ratebooks._meta.get_fields(include_hidden=False)][1:]
    selected = {k: v[0] for k, v in dict(request.POST).items()}
    rbQuery = Q()
    if selected.get('Carrier') != '' and selected.get('Carrier') is not None:
        rbQuery &= Q(Carrier_id=selected.get('Carrier'))
    if selected.get('StateCode') != '' and selected.get('StateCode') is not None:
        rbQuery &= Q(State_id=selected.get('StateCode'))
    if selected.get('UwCompany') != '' and selected.get('UwCompany') is not None:
        rbQuery &= Q(UwCompany_id=selected.get('UwCompany'))
    if selected.get('LineOfBusiness') != '' and selected.get('LineOfBusiness') is not None:
        rbQuery &= Q(LoBusiness_id=selected.get('LineOfBusiness'))
    if selected.get('PolicyType') != '' and selected.get('PolicyType') is not None:
        rbQuery &= Q(PolicyType_id=selected.get('PolicyType'))
    if selected.get('PolicySubType') != '' and selected.get('PolicySubType') is not None:
        rbQuery &= Q(PolicySubType_id=selected.get('PolicySubType'))
    if selected.get('ProductCode') != '' and selected.get('ProductCode') is not None:
        rbQuery &= Q(ProductCode_id=selected.get('ProductCode'))
    filteredRatebooks = Ratebooks.objects.filter(rbQuery).order_by('id')
    page_number = request.GET.get('page')
    paginator = Paginator(filteredRatebooks, 50)
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    viewForm = ViewRBForm(initial=selected)
    return render(request, "ratemanager/ratebookmanager/view_rb.html", locals())


def viewExhibits(request, rbID):
    options = ['createRB', 'viewRB']
    appLabel = 'ratemanager'
    selected = {k: v[0] for k, v in dict(request.POST).items()}
    if request.method == 'GET':
        selected['Exhibit'] = ''
    SelectedRB = Ratebooks.objects.get(pk=rbID)
    selected['Ratebook'] = SelectedRB
    Query = Q()
    Query &= Q(Ratebook=SelectedRB)
    if selected.get('Exhibit') != '':
        Query &= Q(Exhibit=selected.get('Exhibit'))
    filteredExhibits = AllExhibits.objects.filter(Query).order_by('id').values_list()
    fields = [f.name for f in AllExhibits._meta.get_fields(include_hidden=False)]
    exhibitForm = SelectExhibitForm(initial=selected)
    page_number = request.GET.get('page')
    paginator = Paginator(filteredExhibits, 1000)
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request, "ratemanager/ratebookmanager/view_exhibits.html", locals())
