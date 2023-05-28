from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from cart.models import CartItem
from cart.views import _cart_id
from category.models import Category
from orders.models import OrderProduct
from product.forms import ReviewForm
from product.models import Product, ReviewRating
from django.core.paginator import Paginator
from wishlist.models import WishlistItem
from wishlist.views import _wishlist_id


def products_by_category(request, category_slug=None):
    categories = None

    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        if 'min_price' in request.GET:
            filter_price1 = request.GET.get('min_price')
            filter_price2 = request.GET.get('max_price')
            if filter_price1 == '':
                filter_price1 = 0
            products = Product.objects.filter(price__range=(filter_price1, filter_price2), category=categories)
        paginator = Paginator(products, 8)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        if 'min_price' in request.GET:
            filter_price1 = request.GET.get('min_price')
            filter_price2 = request.GET.get('max_price')
            if filter_price1 == '':
                filter_price1 = 0
            products = Product.objects.filter(price__range=(filter_price1, filter_price2))
        paginator = Paginator(products, 8)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,
        'categories': categories,
    }

    return render(request, 'product/product_by_category.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
        if request.user.is_authenticated:
            in_wishlist = WishlistItem.objects.filter(product=single_product, user=request.user).exists()
        else:
            in_wishlist = WishlistItem.objects.filter(wishlist__session=_wishlist_id(request),
                                                      product=single_product).exists()
    except Exception as e:
        raise e
    if request.user.is_authenticated:
        try:
            order_product = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            order_product = None
    else:
        order_product = 0

    # Get the reviews
    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'order_product': order_product,
        'reviews': reviews,
        'in_wishlist': in_wishlist,
    }
    return render(request, 'product/product_detail.html', context)


def search(request):
    products = 0
    product_count = 0
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('created_date').filter(
                Q(product_name__icontains=keyword) | Q(description__icontains=keyword))
            product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count
    }
    return render(request, 'product/product_by_category.html', context)


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)  # submit_review - update the initial review
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)
