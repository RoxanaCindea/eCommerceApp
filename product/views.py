from django.shortcuts import get_object_or_404, render
from cart.models import CartItem
from cart.views import _cart_id
from category.models import Category
from product.models import Product
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


# class ProductListView(ListView):
#     template_name = 'product/all_products.html'
#     model = Product
#     context_object_name = 'all_products'
#
#     # def get_queryset(self):
#     #     return Product.objects.all().filter(is_available=True)
#
#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)
#         context['all_products'] = context['all_products'].all().filter(is_available=True)
#         context['count'] = context['all_products'].filter(is_available=True).count()
#
#         return context


def products_by_category(request, category_slug=None):
    categories = None
    products = None

    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        count = products.count()

    context = {
        'products': paged_products,
        'count': count,
        'categories': categories,
    }

    return render(request, 'product/product_by_category.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
    }
    return render(request, 'product/product_detail.html', context)
