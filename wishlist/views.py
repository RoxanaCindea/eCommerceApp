from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from product.models import Product
from wishlist.models import Wishlist, WishlistItem


def _wishlist_id(request):
    wishlist = request.session.session_key
    if not wishlist:
        wishlist = request.session.create()
    return wishlist


def add_wishlist(request, product_id):
    product = Product.objects.get(id=product_id)  # get the product

    if request.user.is_authenticated:
        is_wishlist_item_exists = WishlistItem.objects.filter(product=product, user=request.user).exists()
        if is_wishlist_item_exists:
            wishlist_item = WishlistItem.objects.filter(product=product, user=request.user)
            wishlist_item.save()
        else:
            wishlist_item = WishlistItem.objects.create(product=product, user=request.user)
            wishlist_item.save()
        return redirect('wishlist')
    else:
        try:
            # get the wishlist using the wishlist_id present in the session
            wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
        except Wishlist.DoesNotExist:
            wishlist = Wishlist.objects.create(wishlist_id=_wishlist_id(request))
        wishlist.save()

        is_wishlist_item_exists = WishlistItem.objects.filter(product=product, user=request.user).exists()
        if is_wishlist_item_exists:
            wishlist_item = WishlistItem.objects.filter(product=product, wishlist=wishlist)
            wishlist_item.save()
        else:
            wishlist_item = WishlistItem.objects.create(product=product, wishlist=wishlist)
            wishlist_item.save()
        return redirect('wishlist')


def remove_wishlist_item(request, product_id, wishlist_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        wishlist_item = WishlistItem.objects.get(product=product, user=request.user, id=wishlist_item_id)
    else:
        wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
        wishlist_item = WishlistItem.objects.get(product=product, wishlist=wishlist, id=wishlist_item_id)
    wishlist_item.delete()
    return redirect('wishlist')


def wishlist_view(request, wishlist_items=0):
    try:
        if request.user.is_authenticated:
            wishlist_items = WishlistItem.objects.filter(user=request.user, is_active=True)
        else:
            wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
            wishlist_items = WishlistItem.objects.filter(wishlist=wishlist, is_active=True)

    except ObjectDoesNotExist:
        pass  # just ignore

    context = {
        'wishlist_items': wishlist_items,
    }
    return render(request, 'wishlist/wishlist.html', context)
