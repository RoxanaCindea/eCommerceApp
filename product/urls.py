from django.urls import path
from product import views

urlpatterns = [
    path('all_products/', views.ProductListView.as_view(), name='all-products'),
    path('<slug:category_slug>/', views.products_by_category, name='products-by-category'),
    path('<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product-detail'),
]
