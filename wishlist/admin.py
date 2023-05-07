from django.contrib import admin
from wishlist.models import Wishlist, WishlistItem


class WishlistAdmin(admin.ModelAdmin):
    list_display = ('wishlist_id', 'date_added')


class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'wishlist', 'is_active')


admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(WishlistItem, WishlistItemAdmin)

