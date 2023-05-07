from .models import Wishlist, WishlistItem
from .views import _wishlist_id


def counter(request):
    if 'admin' in request.path:
        return {}
    else:
        try:
            wishlist = Wishlist.objects.filter(wishlist_id=_wishlist_id(request))
            if request.user.is_authenticated:
                wishlist_items = WishlistItem.objects.all().filter(user=request.user)
            else:
                wishlist_items = WishlistItem.objects.all().filter(wishlist=wishlist)

            wishlist_count = wishlist_items.count()
            print(wishlist_count)
        except Wishlist.DoesNotExist:
            wishlist_count = 0

    return dict(wishlist_count=wishlist_count)
