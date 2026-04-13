from django.urls import path

from backend import views_payment
from . import views

urlpatterns = [
    path('dashboard/', views.ecom_dashboard, name='dashboard'),
    path ('brand-list/', views.brand, name='brand'),
    path('add-brand/', views.add_brand, name='add_new_brand'),
    path('category-list/', views.category_list, name='category'),
    path('product-list/', views.product_list, name='product'),
    path('add-product/', views.add_product, name='add_new_product'),

    path('', views.home, name='home'),
    #Products Information
    path('products/', views.product_web_list, name='product_web_list'),
    path('products/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),

    path('login/', views.login_view, name='user_login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='user_logout'),
    path('request-otp/', views.request_otp_view, name='request_otp'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),

    path('add-or-update-cart/', views.add_or_update_cart, name='add_or_update_cart'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    
     #Payment
    path('payment/success/<str:str_data>/', views_payment.payment_complete, name='payment_complete'),
    path('payment/cancel/<str:str_data>/', views_payment.payment_cancel, name='payment_cancel'),
    path('payment/failed/<str:str_data>/', views_payment.payment_failed, name='payment_failed'),
    path('payment/check/<str:str_data>/', views_payment.payment_check, name="payment_check"),

]