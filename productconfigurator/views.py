from django.shortcuts import render


def productpage(request):
    return render(request, "productconfigurator/product.html", {'title': 'Product', 'heading': ''})
