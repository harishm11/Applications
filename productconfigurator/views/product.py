from django.shortcuts import render, redirect
from django.apps import apps
from ..forms import ProductForm

Productmodel = apps.get_model('productconfigurator', 'Productmodel')
Carriermodel = apps.get_model('productconfigurator', 'Carriermodel')
product_fields = Productmodel._meta.fields


def product_list(request):
    try:
        return render(request, 'productconfigurator/productlist.html', {'products': Productmodel.objects.all(), 'editing_id': None, 'product_fields': product_fields})
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
        return render(request, 'productconfigurator/productadd.html', {'products': Productmodel.objects.all(), 'editing_id': None, 'product_form': product_form})
    except Exception as err:
        return render(request, 'error.html', {'message': err})


def product_edit(request, pk):
    try:
        product = Productmodel.objects.get(pk=pk)
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
        product = Productmodel.objects.get(pk=pk)
        product.delete()
        return render(request, 'productconfigurator/productlist.html', {'products': Productmodel.objects.all(), 'editing_id': None, 'product_fields': product_fields})
    except Exception as err:
        return render(request, 'error.html', {'message': err})
