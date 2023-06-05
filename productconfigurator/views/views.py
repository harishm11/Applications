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

    view_functions = ['createproduct', 'filterproduct']
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
                product = product_form.save()

                product_created = True
                created_product = product

                return redirect('filterproduct')

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
                product = product_form.save()

                product_updated = True
                updated_product = product

                return redirect('filterproduct')
            else:
                redirect(
                    request, 'error.html', {'message': 'Form Error'})

        else:
            product_form = ProductForm(
                request.POST or None, instance=product)

            updated_product = product

        return render(request, 'productconfigurator/updateproduct.html', {
            'product_form': product_form,
            'product_updated': product_updated,
            'updated_product': updated_product,
            'title': 'Update Product'
        })
    except Exception as err:
        return render(request, 'error.html', {'message': err})


def filterProduct(request):
    Model = Product
    # model_fields = [field.name for field in Model._meta.fields]
    model_fields = [field.name for field in Model._meta.get_fields(
        include_hidden=False) if field.name not in ['coverages', 'discounts', 'surcharges', 'id', 'CreateTime', 'UpdateTime',
                                                    'OpenBookInd', 'OpenBookStartDate', 'CloseBookEndDate']]
    form = ProductFilterForm(request.GET or None)
    objectsall = []
    objectsall = Model.objects.none()
    if form.is_valid():
        filter_params = {k: v for k,
                         v in form.cleaned_data.items() if v is not None and v != ''}

        objectsall = Product.objects.filter(**filter_params)

    paginator = Paginator(objectsall, 5)

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
        'model_fields': model_fields,
        'title': 'View Product',
        'coverages': 'CoverageName',
        'discounts': 'DiscountName',
        'surcharges': 'SurchargeName',

    }
    return render(request, 'productconfigurator/filterproduct.html', context)


def viewProduct(request, product_id):
    try:
        Model = Product
        model_fields = [
            field.name for field in Model._meta.get_fields(include_hidden=False)]
        object = get_object_or_404(Product, pk=product_id)
        context = {
            'object': object,
            'model_fields': model_fields,
            'title': 'View Product',
            'coverages': 'CoverageName',
            'discounts': 'DiscountName',
            'surcharges': 'SurchargeName',
        }
        return render(request, 'productconfigurator/viewproduct.html', context)
    except Exception as err:
        return render(request, 'error.html', {'message': err})


def deleteProduct(request, product_id):
    try:
        product = get_object_or_404(Product, pk=product_id)

        if request.method == 'POST':
            product.delete()
            return redirect('filterproduct')

        return render(request, 'productconfigurator/deleteproduct.html', {
            'product': product,
            'title': 'Delete Product'
        })
    except Exception as err:
        return render(request, 'error.html', {'message': err})


def cloneProduct(request, product_id):
    try:
        product = get_object_or_404(Product, pk=product_id)

        if request.method == 'POST':
            product.pk = None  # Create a new object with a new primary key
            product_form = ProductForm(request.POST, instance=product)
            if product_form.is_valid():
                cloned_product = product_form.save()
                return redirect('filterproduct')

        product_form = ProductForm(instance=product)

        return render(request, 'productconfigurator/cloneproduct.html', {
            'product_form': product_form,
            'product': product,
            'title': 'Clone Product'
        })
    except Exception as err:
        return render(request, 'error.html', {'message': err})
