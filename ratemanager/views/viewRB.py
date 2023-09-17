from django.db.models import Q
from django.shortcuts import render
from ratemanager.models import RatebookMetadata
from ratemanager.forms import ViewRBForm, ViewRBFormWithDate, SelectExhibitForm, SelectExhibitFormWithDate
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import ratemanager.views.HelperFunctions as helperfuncs
from datetime import datetime
from django.utils.html import format_html


def viewRB(request):
    options = helperfuncs.SIDEBAR_OPTIONS
    appLabel = 'ratemanager'
    return render(request, 'ratemanager/ratebookmanager/view_rb.html', locals())


def buildViewFilterQuery(selected: dict):
    '''
    Builds a query joined by '&' on Carrier, State, Company
    Business, Policy Type, Sub Type, Product Code.

    'selected' is a dictionay containing the request data of filter form.
    '''
    rbQuery = Q()
    if selected.get('Carrier') != '' and selected.get('Carrier') is not None:
        rbQuery &= Q(Carrier_id=selected.get('Carrier'))
    if selected.get('StateCode') != '' and selected.get('StateCode') is not None:
        rbQuery &= Q(State_id=selected.get('StateCode'))
    if selected.get('UwCompany') != '' and selected.get('UwCompany') is not None:
        rbQuery &= Q(UwCompany_id=selected.get('UwCompany'))
    if selected.get('LineofBusiness') != '' and selected.get('LineofBusiness') is not None:
        rbQuery &= Q(LineofBusiness_id=selected.get('LineofBusiness'))
    if selected.get('PolicyType') != '' and selected.get('PolicyType') is not None:
        rbQuery &= Q(PolicyType_id=selected.get('PolicyType'))
    if selected.get('PolicySubType') != '' and selected.get('PolicySubType') is not None:
        rbQuery &= Q(PolicySubType_id=selected.get('PolicySubType'))
    if selected.get('ProductCode') != '' and selected.get('ProductCode') is not None:
        rbQuery &= Q(ProductCode_id=selected.get('ProductCode'))

    return rbQuery


def viewRBbyVersion(request):
    options = helperfuncs.SIDEBAR_OPTIONS
    appLabel = 'ratemanager'
    selected = {k: v[0] for k, v in dict(request.POST).items()}
    rbQuery = buildViewFilterQuery(selected=selected)
    filteredRatebookMetadata = RatebookMetadata.objects.filter(rbQuery).order_by('id')
    page_number = request.GET.get('page')
    paginator = Paginator(filteredRatebookMetadata, 50)
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
    rbQuery = buildViewFilterQuery(selected=selected)
    filteredRatebookMetadata = RatebookMetadata.objects.filter(rbQuery).order_by('RatebookID').distinct('RatebookID')
    page_number = request.GET.get('page')
    paginator = Paginator(filteredRatebookMetadata, 50)
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
