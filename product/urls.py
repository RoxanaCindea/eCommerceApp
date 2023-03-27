from django.urls import path
from product import views

urlpatterns = [
    path('all_products/', views.ProductListView.as_view(), name='all-products'),
    path('<slug:category_slug>/', views.products_by_category, name='products-by-category'),
]