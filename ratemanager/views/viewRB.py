from django.db.models import Q
from django.shortcuts import render
from ratemanager.models import Ratebooks
from ratemanager.forms import ViewRBForm, ViewRBFormWithDate, SelectExhibitForm, SelectExhibitFormWithDate
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import ratemanager.views.HelperFunctions as helperfuncs
from datetime import datetime
from django.utils.html import format_html


def viewRB(request):
    options = helperfuncs.SIDEBAR_OPTIONS
    appLabel = 'ratemanager'
    return render(request, 'ratemanager/ratebookmanager/view_rb.html', locals())


def viewRBbyVersion(request):
    options = helperfuncs.SIDEBAR_OPTIONS
    appLabel = 'ratemanager'
    selected = {k: v[0] for k, v in dict(request.POST).items()}
    rbQuery = helperfuncs.buildViewFilterQuery(selected=selected)
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
    return render(request, "ratemanager/ratebookmanager/viewRBbyVersion.html", locals())


def viewRBbyVersionExhibits(request, rbID, rbVer):
    options = helperfuncs.SIDEBAR_OPTIONS
    appLabel = 'ratemanager'
    selected = {k: v[0] for k, v in dict(request.POST).items()}
    if request.method == 'GET':
        selected['Exhibit'] = ''
        selected['PivotView'] = 'on'
    selected['RatebookID'] = rbID
    Query = Q()
    Query &= Q(RatebookID=rbID)
    if selected.get('Exhibit') != '':
        Query &= Q(Exhibit=selected.get('Exhibit'))
    filteredExhibits = helperfuncs.fetchRatebookSpecificVersion(rbID=rbID, rbVersion=rbVer).\
        order_by('Coverage', 'Exhibit').filter(Query)
    exhibitForm = SelectExhibitForm(initial=selected)
    pivotview = selected['PivotView']
    if pivotview == 'on' and selected.get('Exhibit') != '':
        df = helperfuncs.convert2Df(filteredExhibits)
        idf = helperfuncs.inverseTransform(df)
        idf = idf.fillna('')
        dfHTML = format_html(idf.to_html(table_id='example', index=False))
    else:
        page_number = request.GET.get('page')
        paginator = Paginator(filteredExhibits, 1000)
        try:
            page_obj = paginator.get_page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
    return render(request, "ratemanager/ratebookmanager/viewRBbyVersionExhibits.html", locals())


def viewRBbyDate(request):
    options = helperfuncs.SIDEBAR_OPTIONS
    appLabel = 'ratemanager'
    selected = {k: v[0] for k, v in dict(request.POST).items()}
    rbQuery = helperfuncs.buildViewFilterQuery(selected=selected)
    filteredRatebooks = Ratebooks.objects.filter(rbQuery).distinct('RatebookID')
    page_number = request.GET.get('page')
    paginator = Paginator(filteredRatebooks, 50)
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    viewForm = ViewRBFormWithDate(initial=selected)
    return render(request, "ratemanager/ratebookmanager/viewRBbyDate.html", locals())


def viewRBbyDateExhibits(request, rbID):
    options = helperfuncs.SIDEBAR_OPTIONS
    appLabel = 'ratemanager'
    selected = {k: v[0] for k, v in dict(request.POST).items()}
    if request.method == 'GET':
        selected['Exhibit'] = ''
        selected['QueryDate'] = datetime.today()
    selected['RatebookID'] = rbID
    Query = Q()
    Query &= Q(RatebookID=rbID)
    if selected.get('Exhibit') != '':
        Query &= Q(Exhibit=selected.get('Exhibit'))
    filteredExhibits = helperfuncs.fetchRatebookbyDate(rbID=rbID, qDate=selected.get('QueryDate')).\
        order_by('Coverage', 'Exhibit').filter(Query)
    exhibitForm = SelectExhibitFormWithDate(initial=selected)
    page_number = request.GET.get('page')
    paginator = Paginator(filteredExhibits, 1000)
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request, "ratemanager/ratebookmanager/viewRBbyDateExhibits.html", locals())
