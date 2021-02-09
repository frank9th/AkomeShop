from django.contrib import admin
from django.urls import path, include
from . import views 


urlpatterns = [
	path('',views.homePage, name='home'),
	path('cart/',views.cart, name='cart'),
	path('checkout/',views.checkout, name='checkout'),
	path('product/<slug>/', views.productDetailView, name='product'),
	path('add-to-cart/<slug>/', views.add_to_cart, name='add-to-cart'),
	#path('add-to-cart/<int:pk>/', views.add_to_cart, name='add-to-cart'),
	path('add-coupon', views.add_coupon, name='add-coupon'),
	#path('remove-form-cart/<slug>/', views.remove_form_cart, name='remove-form-cart'),
	path('remove-form-cart/<int:pk>/', views.remove_form_cart, name='remove-form-cart'),
	#path('remove-single-item/<slug>/', views.remove_single_item, name='remove-single-item'),
	path('remove-single-item/<int:pk>/', views.remove_single_item, name='remove-single-item'),
	path('order-summary/', views.OrderSummary, name='order-summary'),
	path('order-form/',views.createOrder, name='order-form'),
	path('update_order/<str:pk>/',views.updateOrder, name='update_order'), # passing in the primary key of the request objet into the url
	path('delete_item/<str:pk>/',views.delete_item, name='delete_order'),
	path('payment/<payment_option>/', views.paymentPage, name='payment'),
	path('request-refund', views.RequestRefund, name='request-refund')
]

