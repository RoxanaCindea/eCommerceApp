from django.shortcuts import render
from django.views.generic import TemplateView
from product.models import Product


def home(request):
    products = Product.objects.all().filter(is_available=True)

    context = {
        'products': products
    }
    return render(request, 'home/home.html', context)
