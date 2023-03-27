from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

from category.models import Category
from product.models import Product


class ProductListView(ListView):
    template_name = 'product/all_products.html'
    model = Product
    context_object_name = 'all_products'

    # def get_queryset(self):
    #     return Product.objects.all().filter(is_available=True)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['all_products'] = context['all_products'].all().filter(is_available=True)
        context['count'] = context['all_products'].filter(is_available=True).count()

        return context


def products_by_category(request, category_slug=None):
    categories = None
    products = None

    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)

    context = {
        'products': products,
    }

    context['count'] = context['products'].filter(category=categories, is_available=True).count()

    return render(request, 'product/products_by_category.html', context)
