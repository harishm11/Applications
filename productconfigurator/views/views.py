from django.shortcuts import render
from django.urls import get_resolver
from ..forms import ProductForm
from django.shortcuts import render, redirect
from django.apps import apps
from django.db.models import Q
from django.shortcuts import render,  redirect


from productconfigurator.forms import *

coverage = apps.get_model('systemtables', 'coverage')
discount = apps.get_model('systemtables', 'discount')
surcharge = apps.get_model('systemtables', 'surcharge')

# def productconfigurator(request):
#     options = []
#     for model in apps.get_app_config('productconfigurator').get_models():
#         options.append(model.__name__)
#     context = {'options': options, 'appLabel': 'productconfigurator'}
#     return render(request, 'productconfigurator/home.html', context)


def productconfigurator(request):

    view_functions = ['createproduct', 'viewproduct']
    context = {'options': view_functions, 'appLabel': 'productconfigurator'}
    return render(request, 'productconfigurator/home.html', context)


def getModelNames(appLabel):
    options = []
    for model in apps.get_app_config(appLabel).get_models():
        options.append(model.__name__)

    modelnames = {'options': options}
    return modelnames


def createProduct(request):
    try:
        product_created = False
        created_product = None
        selected_coverages = []

        if request.method == 'POST':
            product_form = ProductForm(request.POST)

            if product_form.is_valid():
                product = product_form.save(commit=False)
                selected_coverages_ids = request.POST.getlist('coverages')
                selected_coverages = coverage.objects.filter(
                    id__in=selected_coverages_ids)
                product.save()
                product.coverages.set(selected_coverages)


                selected_discounts_ids = request.POST.getlist('discounts')
                selected_discounts = discount.objects.filter(
                    id__in=selected_discounts_ids)
                product.discounts.set(selected_discounts)

                selected_surcharges_ids = request.POST.getlist('surcharges')
                selected_surcharges = surcharge.objects.filter(
                    id__in=selected_surcharges_ids)
                product.surcharges.set(selected_surcharges)


                product_created = True
                created_product = product

                return redirect('viewproduct')
            else:
                coverages = coverage.objects.all().order_by('CoverageName', 'Amount1')
                discounts = discount.objects.all().order_by('DiscountName')
                surcharges = surcharge.objects.all().order_by('SurchargeName')
        else:
            product_form = ProductForm()
            coverages = coverage.objects.all().order_by('CoverageName', 'Amount1')
            discounts = discount.objects.all().order_by('DiscountName')
            surcharges = surcharge.objects.all().order_by('SurchargeName')

        return render(request, 'productconfigurator/createproduct.html', {
            'product_form': product_form,
            'coverages': coverages,
            'discounts': discounts,
            'surcharges': surcharges,
            'product_created': product_created,
            'created_product': created_product,
            'selected_coverages': selected_coverages
        })
    except Exception as err:
        return render(request, 'error.html', {'message': err})


def viewProduct(request):
    try:
        Model = product
        model_fields = [field.name for field in Model._meta.fields]

        verboseNamePlural = Model._meta.verbose_name_plural
        search_query = request.GET.get('search', '')
        if search_query:
            q_objects = Q()
            for field in model_fields:
                q_objects |= Q(**{f'{field}__icontains': search_query})
            objects = Model.objects.filter(q_objects)
        else:
            objects = Model.objects.all()

        context = {
            'Model': Model,
            'model_fields': model_fields,
            'objects': objects,
            'verboseNamePlural_value': verboseNamePlural,
            'search_query': search_query,
        }

        return render(request, 'productconfigurator/viewproduct.html', context)
    except Exception as err:
        return render(request, 'error.html', {'message': err})
