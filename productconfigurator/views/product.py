from django.shortcuts import render, redirect
from django.apps import apps
from ..forms.product import ProductForm

Product = apps.get_model(
    'productconfigurator', 'Product')
carrier = apps.get_model('productconfigurator', 'carrier')
coverage = apps.get_model('productconfigurator', 'coverage')
product_fields = Product._meta.fields


def product_list(request):
    try:
        return render(request, 'productconfigurator/productlist.html', {'products': Product.objects.all(), 'editing_id': None, 'product_fields': product_fields})
    except Exception as err:
        return render(request, 'error.html', {'message': err})


def product_add(request):
    try:
        if request.method == 'POST':
            product_form = ProductForm(request.POST)
            if product_form.is_valid():
                product_form.save()
                return redirect('product_list')
        else:
            product_form = ProductForm()
        return render(request, 'productconfigurator/productadd.html', {'products': Product.objects.all(), 'editing_id': None, 'product_form': product_form})
    except Exception as err:
        return render(request, 'error.html', {'message': err})


def product_edit(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        product_form = ProductForm(request.POST, instance=product)
        if product_form.is_valid():
            product_form.save()
            return redirect('product_list')
        else:
            product_form = ProductForm(instance=product)
        return render(request, 'productconfigurator/productedit.html', {'product_form': product_form})
    except Exception as err:
        return render(request, 'error.html', {'message': err})


def product_delete(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        product.delete()
        return render(request, 'productconfigurator/productlist.html', {'products': Product.objects.all(), 'editing_id': None, 'product_fields': product_fields})
    except Exception as err:
        return render(request, 'error.html', {'message': err})


def product_add_coverages(request):
    try:
        coverage = coverage.objects.all()
        return render(request, 'productconfigurator/coveragelist.html', {'coverage': coverage})
    except Exception as err:
        return render(request, 'error.html', {'message': err})
