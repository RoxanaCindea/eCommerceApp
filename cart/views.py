from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from cart.models import Cart, CartItem
from product.models import Product


def _cart_id(request):
    cart_session = request.session.session_key
    if not cart_session:
        cart_session = request.session.create()
    return cart_session


def add_cart(request, product_id):
    color = request.GET['color']
    size = request.GET['size']
    product = Product.objects.get(id=product_id)  # get the product

    try:
        cart_session = Cart.objects.get(
            cart_id=_cart_id(request))  # get the cart using the cart_id present in the session
    except Cart.DoesNotExist:
        cart_session = Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart_session.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart_session)
        cart_item.quantity += 1  # cart_item.quantity = cart_item.quantity
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart_session,
        )
        cart_item.save()
    return redirect('cart')


def remove_cart(request, product_id):
    cart_session = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart_session)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


def remove_cart_item(request, product_id):
    cart_session = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart_session)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=0, tax=0, grant_total=0):
    try:
        cart_session = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart_session, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (2 * total) / 100
        grant_total = total + tax

    except ObjectDoesNotExist:
        pass  # just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grant_total,
    }
    return render(request, 'cart/cart.html', context)
