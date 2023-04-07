from django.urls import path
from product import views

urlpatterns = [
    path('all_products/', views.products_by_category, name='all-products'),
    path('category/<slug:category_slug>/', views.products_by_category, name='products-by-category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product-detail'),
    path('search/', views.search, name='search'),
]
