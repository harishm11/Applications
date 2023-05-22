# from ..forms import ProductForm
from django.shortcuts import render
from django.urls import get_resolver
from ..forms import ProductForm
from django.shortcuts import render, get_object_or_404, redirect
from django.apps import apps
from django.db.models import Q
from django.shortcuts import render,  redirect
from django.forms import modelform_factory
from ..models.product import Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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

        if request.method == 'POST':
            product_form = ProductForm(request.POST)

            if product_form.is_valid():
                product = product_form.save(commit=False)
                # selected_option_values = request.POST.getlist('options')
                # selected_coverages = coverage.objects.filter(
                #     OptionValue__in=selected_option_values)
                # product.save()
                # product.coverages.set(selected_coverages)

                # selected_discounts_ids = request.POST.getlist('discounts')
                # selected_discounts = discount.objects.filter(
                #     id__in=selected_discounts_ids)
                # product.discounts.set(selected_discounts)

                # selected_surcharges_ids = request.POST.getlist('surcharges')
                # selected_surcharges = surcharge.objects.filter(
                #     id__in=selected_surcharges_ids)
                # product.surcharges.set(selected_surcharges)

                product_created = True
                created_product = product

                return redirect('viewproduct')

        else:
            product_form = ProductForm()

        return render(request, 'productconfigurator/createproduct.html', {
            'product_form': product_form,
            'product_created': product_created,
            'created_product': created_product,
            'title': 'Create Product'
        })
    except Exception as err:
        return render(request, 'error.html', {'message': err})


def updateProduct(request, product_id):
    try:
        product_updated = False
        updated_product = None
        selected_coverages = []

        product = get_object_or_404(Product, pk=product_id)

        if request.method == 'POST':
            product_form = ProductForm(
                request.POST or None, instance=product)

            if product_form.is_valid():
                product = product_form.save(commit=False)
                # selected_option_values = request.POST.getlist('options')
                # selected_coverages = coverage.objects.filter(
                #     OptionValue__in=selected_option_values)
                # product.save()
                # product.coverages.set(selected_coverages)

                # selected_discounts_ids = request.POST.getlist('discounts')
                # selected_discounts = discount.objects.filter(
                #     id__in=selected_discounts_ids)
                # product.discounts.set(selected_discounts)

                # selected_surcharges_ids = request.POST.getlist('surcharges')
                # selected_surcharges = surcharge.objects.filter(
                #     id__in=selected_surcharges_ids)
                # product.surcharges.set(selected_surcharges)

                product_updated = True
                updated_product = product

                return redirect('viewproduct')
            else:
                redirect(
                    request, 'error.html', {'message': 'Form Error'})

        else:
            product_form = ProductForm(
                request.POST or None, instance=product)

            updated_product = product
            coverages = coverage.objects.all().order_by('CoverageName', 'Amount1')
            discounts = discount.objects.all().order_by('DiscountName')
            surcharges = surcharge.objects.all().order_by('SurchargeName')
            selected_coverages = product.coverages.all
            selected_discounts = product.discounts.all
            selected_surcharges = product.surcharges.all

            selected_coverage_options = [
                (c.CoverageName, c.OptionValue) for c in selected_coverages()]
        return render(request, 'productconfigurator/updateproduct.html', {
            'product_form': product_form,
            'coverages': coverages,
            'discounts': discounts,
            'surcharges': surcharges,
            'selected_coverages': selected_coverages,
            'selected_discounts': selected_discounts,
            'selected_surcharges': selected_surcharges,
            'product_updated': product_updated,
            'updated_product': updated_product,
            'selected_coverage_options': selected_coverage_options,
            'title': 'Update Product'
        })
    except Exception as err:
        return render(request, 'error.html', {'message': err})


def viewProduct(request):
    Model = product
    model_fields = [field.name for field in Model._meta.fields]
    form = ProductFilterForm(request.GET or None)
    objectsall = []
    objectsall = Model.objects.none()
    if form.is_valid():
        filter_params = {k: v for k,
                         v in form.cleaned_data.items() if v is not None and v != ''}

        objectsall = Product.objects.filter(**filter_params)

    paginator = Paginator(objectsall, 1)

    page = request.GET.get('page')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    context = {
        'form': form,
        'objects': objects,
        'model_fields': model_fields
    }
    return render(request, 'productconfigurator/viewproduct.html', context)
