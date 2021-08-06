from django.urls import path
from . import views 

from .views import (
    ItemDetailView,
    CheckoutView,
    HomeView,
    OrderSummaryView,
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
    PaymentView,
    AddCouponView,
    RequestRefundView,

)

app_name = 'store'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product/category/<slug>/', views.product_category, name='category'),
    path('search/', views.search, name='search'),
    path('cart/',views.cart, name='cart'),
    path('confirm-checkout/',views.clientCheckout, name='confirm-checkout'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('product/', views.AddProduct, name='product'),
    path('product-list/', views.ProductList, name='product-list'),
    path('update-product/<str:pk>/', views.UpdateProduct, name='update-product'),
    path('fastfood/<str:code>/', views.FastFood, name= 'seller'),
    path('fastfood/', views.FoodSellers, name= 'fastfood'),
    path('services/', views.ServicePage, name= 'services'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('add-client-details/', views.AddClientCode, name='add-client-details'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('delete_item/<str:pk>/',views.delete_item, name='delete_order'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('request-refund/', RequestRefundView.as_view(), name='request-refund')
]


