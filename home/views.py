from django.shortcuts import render
from product.models import Product, ReviewRating


def home(request):
    products = Product.objects.filter(is_available=True, ).order_by('created_date').all()[:4]
    # Get the reviews
    for product in products:
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)
    context = {
        'products': products,
        'reviews': reviews,
    }
    return render(request, 'home/home.html', context)
