# from ..forms import ProductForm
from django.shortcuts import render
from django.urls import get_resolver
from ..forms import ProductForm
from django.shortcuts import render, get_object_or_404, redirect
from django.apps import apps
from django.db.models import Q
from django.shortcuts import render,  redirect
from django.forms import ValidationError
from ..models.product import Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from myproj.utils import handleformerror
from django.forms import formset_factory
from ..forms import ProductForm, ProductCoverageForm, ProductCoverageOptionForm
from productconfigurator.forms import *


coverage = apps.get_model('systemtables', 'coverage')
coverageoptions = apps.get_model('systemtables', 'coverageoptions')
discount = apps.get_model('systemtables', 'discount')
surcharge = apps.get_model('systemtables', 'surcharge')
options = ['createproduct', 'filterproduct']
appLabel = 'productconfigurator'


def productconfigurator(request):
    context = {'options': options, 'appLabel': appLabel}
    return render(request, 'productconfigurator/home.html', context)


def getModelNames(appLabel):
    options = []
    for model in apps.get_app_config(appLabel).get_models():
        options.append(model.__name__)

    modelnames = {'options': options}
    return modelnames


def createProductold(request):
    try:
        context = {}
        error_msg = ''
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
                error_msg = handleformerror(product_form)

        else:
            product_form = ProductForm()
        context = {'options': options, 'appLabel': appLabel,
                   'product_form': product_form,
                   'product_created': product_created,
                   'created_product': created_product,
                   'title': 'Create Product',
                   'message': error_msg
                   }

        return render(request, 'productconfigurator/createproduct.html', context)
    except Exception as err:
        return render(request, 'error.html', {'message': err})


def updateProduct(request, product_id):
    try:
        context = {}
        error_msg = ''
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

                request.session['productid'] = updated_product.id
                request.session['view'] = 'update'
                return redirect('createproductcoverage')
            else:
                updated_product = product
                error_msg = handleformerror(product_form)

        else:
            product_form = ProductForm(
                request.POST or None, instance=product)

            updated_product = product
        context = {'options': options, 'appLabel': appLabel,
                   'product_form': product_form,
                   'product_updated': product_updated,
                   'updated_product': updated_product,
                   'title': 'Update Product',
                   'message': error_msg
                   }

        return render(request, 'productconfigurator/updateproduct.html', context
                      )
    except Exception as err:
        return render(request, 'error.html', {'message': err})


def filterProduct(request):
    context = {}
    error_msg = ''
    Model = Product
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
    else:
        error_msg = handleformerror(form)
    paginator = Paginator(objectsall, 5)

    page = request.GET.get('page')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    context = {
        'options': options,
        'appLabel': appLabel,
        'form': form,
        'objects': objects,
        'model_fields': model_fields,
        'title': 'View Product',
        'coverages': 'CoverageName',
        'discounts': 'DiscountName',
        'surcharges': 'SurchargeName',
        'message': error_msg

    }
    return render(request, 'productconfigurator/filterproduct.html', context)


def viewProduct(request, product_id):
    try:
        context = {}
        Model = Product

        product_fields = [
            field.name for field in Model._meta.get_fields(include_hidden=False)]
        Model = ProductCoverage

        product_coverage_fields = [
            field.name for field in Model._meta.get_fields(include_hidden=False)]
        Model = ProductCoverageOption

        product_coverage_option_fields = [
            field.name for field in Model._meta.get_fields(include_hidden=False)]
        product = Product.objects.get(pk=product_id)
        product_coverages = ProductCoverage.objects.filter(product=product)
        product_coverage_options = ProductCoverageOption.objects.filter(
            ProductCoverage__product=product
        )
        context = {
            'options': options,
            'appLabel': appLabel,
            'product': product,
            'product_fields': product_fields,
            'product_coverage_fields': product_coverage_fields,
            'product_coverage_option_fields': product_coverage_option_fields,
            'title': 'View Product',
            'product_coverages': product_coverages,
            'product_coverage_options': product_coverage_options,
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
            'options': options,
            'product': product,
            'title': 'Delete Product',

        })
    except Exception as err:
        return render(request, 'error.html', {'message': err})


def cloneProduct(request, product_id):
    try:
        context = {}
        error_msg = ''
        product = get_object_or_404(Product, pk=product_id)
        # coverages = ProductCoverage.objects.filter(product=product)
        if request.method == 'POST':
            product.pk = None

            # Create a new object with a new primary key
            product_form = ProductForm(request.POST, instance=product)

            if product_form.is_valid():
                cloned_product = product_form.save()
                request.session['productid'] = cloned_product.id
                request.session['view'] = 'clone'
                return redirect('createproductcoverage')

            else:
                error_msg = handleformerror(product_form)

        product_form = ProductForm(instance=product)
        context = {
            'options': options,
            'appLabel': appLabel,
            'product_form': product_form,
            'product': product,
            'title': 'Clone Product',
            'message': error_msg

        }
        return render(request, 'productconfigurator/cloneproduct.html', context

                      )
    except Exception as err:
        return render(request, 'error.html', {'message': err})


def createProduct(request):
    error_msg = ''
    if request.method == 'POST':
        product_form = ProductForm(request.POST)

        if product_form.is_valid():
            product_info = product_form.cleaned_data
            created_product = product_form.save()
            request.session['productid'] = created_product.id
            return redirect('createproductcoverage')
        else:
            error_msg = handleformerror(product_form)

    else:
        product_form = ProductForm()

    return render(request, 'productconfigurator/createProduct.html', {'product_form': product_form, 'message': error_msg, 'title': 'Create Product', })


def createProductCoverage(request):
    error_msg = ''
    if 'productid' not in request.session:
        return redirect('createproduct')

    if request.method == 'POST':

        coverage_form = ProductCoverageForm(request.POST)

        if coverage_form.is_valid():
            selected_coverages = coverage_form.cleaned_data['coverages']
            product = Product.objects.get(id=request.session['productid'])
            for coverage in selected_coverages:
                product_coverage = ProductCoverage.objects.create(
                    product=product,
                    CoverageName=coverage,
                    EffectiveDate=product.EffectiveDate,
                    ExpiryDate=product.ExpiryDate,
                )

            selected_coverage_ids = [
                coverage.id for coverage in selected_coverages]
            request.session['selected_coverage_ids'] = selected_coverage_ids

            return redirect('createcoverageoptns')
        else:
            error_msg = handleformerror(coverage_form)
    else:
        if request.session['view'] == 'update' or request.session['view'] == 'clone':
            product = Product.objects.get(id=request.session['productid'])
            product_coverages = ProductCoverage.objects.filter(product=product)

            # Extract the coverages from the queryset
            coverages = [pc.CoverageName for pc in product_coverages]

            # Initial data for the form
            initial_data = {
                'coverages': coverages,
                # You may need to adjust this based on your model
                'EffectiveDate': product.EffectiveDate,
                # You may need to adjust this based on your model
                'ExpiryDate': product.ExpiryDate,
            }

            # Create the form and pass the initial data
            coverage_form = ProductCoverageForm(initial=initial_data)
        else:
            coverage_form = ProductCoverageForm()

    return render(request, 'productconfigurator/createProductCoverage.html', {'coverage_form': coverage_form, 'message': error_msg, 'title': 'Select Coverages'})


def createCoverageOptns(request):
    error_msg = ''
    if 'selected_coverage_ids' not in request.session:
        return redirect('createproductcoverage')

    selected_coverage_ids = request.session['selected_coverage_ids']
    selected_coverages = coverage.objects.filter(id__in=selected_coverage_ids)
    coverage_options = coverageoptions.objects.filter(
        CoverageName__in=selected_coverage_ids)
    options_list = [(f"{option.CoverageName} - {option.OptionValue}",
                     f"{option.CoverageName} - {option.OptionValue}") for option in coverage_options]
    product = Product.objects.get(id=request.session['productid'])
    if request.method == 'POST':
        coverage_option_form = ProductCoverageOptionForm(
            request.POST, options=options_list)

        if coverage_option_form.is_valid():
            selected_coverage_options = request.POST.getlist(
                'selected_options')
            for covid in selected_coverage_ids:
                for option in selected_coverage_options:
                    coverage_name, option_value = option.split(' - ')

                    cov = ProductCoverage.objects.get(
                        CoverageName_id=covid, product_id=product.id)
                    if coverage_name == cov.CoverageName.CoverageName:
                        covoption = coverageoptions.objects.get(
                            CoverageName_id=covid, OptionValue=option_value)

                        ProductCoverageOption.objects.create(
                            ProductCoverage=cov,
                            OptionValue=covoption,
                            EffectiveDate=product.EffectiveDate,
                            ExpiryDate=product.ExpiryDate,
                        )

            del request.session['productid']
            del request.session['selected_coverage_ids']

            return redirect('filterproduct')
        else:
            error_msg = handleformerror(coverage_option_form)
    else:

        if request.session['view'] == 'update' or request.session['view'] == 'clone':
            product = Product.objects.get(id=request.session['productid'])
            product_coverages = ProductCoverage.objects.filter(product=product)
            sel_cov_options = ProductCoverageOption.objects.filter(
                ProductCoverage__product=product
            )

            # Here you can access the OptionValue for each selected option
            coverage_options = coverageoptions.objects.filter(
                CoverageName__in=selected_coverage_ids)
            options_list = [(f"{option.CoverageName} - {option.OptionValue}",
                             f"{option.CoverageName} - {option.OptionValue}") for option in coverage_options]
            coverage_option_form = ProductCoverageOptionForm(
                options=options_list)
            initial_selected_options = [option.OptionValue
                                        for option in sel_cov_options]
            # coverage_option_form.fields['selected_options'].choices = initial_selected_options

        else:
            coverage_option_form = ProductCoverageOptionForm(options=options_list
                                                             )
    return render(request, 'productconfigurator/createCoverageOptns.html',
                  {'coverage_option_form': coverage_option_form, 'selected_coverages': selected_coverages, 'message': error_msg, 'title': 'Select Coverage Options'})
