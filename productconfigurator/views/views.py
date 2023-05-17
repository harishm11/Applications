from django.shortcuts import render
from django.urls import get_resolver
from ..forms import ProductForm
from django.shortcuts import render, get_object_or_404, redirect
from django.apps import apps
from django.db.models import Q
from django.shortcuts import render,  redirect
from django.forms import modelform_factory
from ..models.product import Product


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
                selected_option_values = request.POST.getlist('options')
                selected_coverages = coverage.objects.filter(
                    OptionValue__in=selected_option_values)
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
            'selected_coverages': selected_coverages,
            'title': 'Create Product'
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
            # Search in the specified model fields
            for field in model_fields:
                q_objects |= Q(**{f'{field}__icontains': search_query})

            # Search in the 'coverages' field
            q_objects |= Q(coverages__CoverageName__icontains=search_query) | Q(
                coverages__OptionValue__icontains=search_query)

            # Search in the 'discounts' field
            q_objects |= Q(discounts__DiscountName__icontains=search_query) | Q(
                discounts__DiscountDesc__icontains=search_query)

            # Search in the 'surcharges' field
            q_objects |= Q(surcharges__SurchargeName__icontains=search_query) | Q(
                surcharges__SurchargeDesc__icontains=search_query)

            objects = Model.objects.filter(q_objects).distinct()
        else:
            objects = Model.objects.all()

        context = {
            'Model': Model,
            'model_fields': model_fields,
            'objects': objects,
            'verboseNamePlural_value': verboseNamePlural,
            'search_query': search_query,
            'title': 'View Products'
        }

        return render(request, 'productconfigurator/viewproduct.html', context)
    except Exception as err:
        return render(request, 'error.html', {'message': err})


def updateProduct(request, product_id):
    try:
        product_updated = False
        updated_product = None
        selected_coverages = []

        # Retrieve the product instance to be updated
        product = get_object_or_404(Product, pk=product_id)
        # product = Product.objects.get(id=product_id)

        form = modelform_factory(Product, exclude=('id', 'coverages', 'discounts', 'surcharges'), widgets={
            'OpenBookStartDate': forms.DateInput(attrs={'type': 'date'}),
            'CloseBookEndDate': forms.DateInput(attrs={'type': 'date'}),
            'EffectiveDate': forms.DateInput(attrs={'type': 'date'}),
            'ExpiryDate': forms.DateInput(attrs={'type': 'date'}),

        })
        if request.method == 'POST':
            product_form = ProductForm(request.POST or None, instance=product)

            if product_form.is_valid():
                product = product_form.save(commit=False)
                selected_option_values = request.POST.getlist('options')
                selected_coverages = coverage.objects.filter(
                    OptionValue__in=selected_option_values)
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

                product_updated = True
                updated_product = product

                context = {
                    'Model': Product,
                    'title': 'View Products'
                }

                redirect(request, 'productconfigurator/viewproduct.html', context)
            else:
                coverages = coverage.objects.all().order_by('CoverageName', 'Amount1')
                discounts = discount.objects.all().order_by('DiscountName')
                surcharges = surcharge.objects.all().order_by('SurchargeName')
        else:
            product_form = form(instance=product)
            updated_product = product
            coverages = coverage.objects.all().order_by('CoverageName', 'Amount1')
            discounts = discount.objects.all().order_by('DiscountName')
            surcharges = surcharge.objects.all().order_by('SurchargeName')
            selected_coverages = product.coverages.all
            selected_discounts = product.discounts.all
            selected_surcharges = product.surcharges.all
            # Execute the method to obtain the queryset
            selected_coverage_options = [
                (c.CoverageName, c.OptionValue) for c in selected_coverages()]
            print(selected_coverage_options)
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
