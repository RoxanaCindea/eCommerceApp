from .models import Wishlist, WishlistItem
from .views import _wishlist_id


def counter_wishlist(request):
    if 'admin' in request.path:
        return {}
    else:
        try:
            wishlist = Wishlist.objects.filter(session=_wishlist_id(request))
            if request.user.is_authenticated:
                wishlist_items = WishlistItem.objects.all().filter(user=request.user)
            else:
                wishlist_items = WishlistItem.objects.all().filter(wishlist=wishlist[:1])
            wishlist_count = wishlist_items.count()

        except Wishlist.DoesNotExist:
            wishlist_count = 0

    return dict(wishlist_count=wishlist_count)
