from django.urls import path

from accounts import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.dashboard, name='dashboard'),

    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forgotPassword/', views.forgot_password, name='forgotPassword'),
    path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),
    path('resetPassword/', views.reset_password, name='resetPassword'),

    path('my_orders/', views.my_orders, name='my_orders'),
    path('order_details/<int:order_id>', views.order_details, name='order_details'),
    path('view_edit_profile/', views.view_edit_profile, name='view_edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
]
