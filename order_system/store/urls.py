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
    #path('', HomeView.as_view(), name='home'),
    path('', views.Home, name='home'),
    path('product/category/<slug>/', views.product_category, name='category'),
    path('search/', views.search, name='search'),
    path('cart/',views.cart, name='cart'),
    path('confirm-checkout/',views.clientCheckout, name='confirm-checkout'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('product/', views.AddProduct, name='product'),
    path('service/provider/<code>/', views.Provider, name='provider'),
    path('product-list/', views.ProductList, name='product-list'),
    path('seller-store/<code>/', views.SellerProduct, name='seller-store'),
    path('update-product/<str:pk>/', views.UpdateProduct, name='update-product'),
    path('update-store', views.UpdateStore, name='update-store'),
    path('fastfood/<str:code>/', views.FastFood, name= 'seller'),
    path('fastfood/', views.FoodSellers, name= 'fastfood'),
    path('services/', views.ServicePage, name= 'services'),
    path('logistics/', views.LogisticPage, name= 'logistics'),
    path('confirm/ref/', views.ConfirmLogistics, name='confirm-ref'),
    path('check/ref/<code>', views.CheckRef, name='check-ref'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('add-client-details/', views.AddClientCode, name='add-client-details'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('delete_item/<str:pk>/',views.delete_item, name='delete_order'),
    path('delete-trans/<str:pk>/',views.delete_trans, name='delete-trans'),
    path('delete-product/<str:pk>/',views.delete_store_product, name='delete-product'),
    #path('cardpay/', views.CardPay, name='cardpay'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('confirm/<int:ref>/', views.verifyPayment, name='confirm'),
    path('request-refund/', RequestRefundView.as_view(), name='request-refund')
]


