from django.db import models
from accounts.models import Account
from product.models import Product


class Wishlist(models.Model):
    session = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.session


class WishlistItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.product
