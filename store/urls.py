from django.contrib import admin
from django.urls import path, include
from . import views 
urlpatterns = [
	#path('sales-home', views.salesHome, name='sales-home'),
	path('',views.homePage, name='home'),
	path('cart/',views.cart, name='cart'),
	path('checout/',views.checkout, name='checkout'),
	path('product/<slug>/', views.productDetailView, name='product'),
	path('add-to-cart/<slug>/', views.add_to_cart, name='add-to-cart'),
	path('remove-form-cart/<slug>/', views.remove_form_cart, name='remove-form-cart'),
	path('order-form/',views.createOrder, name='order-form'),
	path('update_order/<str:pk>/',views.updateOrder, name='update_order'), # passing in the primary key of the request objet into the url
	path('delete_item/<str:pk>/',views.delete_item, name='delete_order'),
	path('add_customer', views.addCustomer, name='add_customer'),
	path('edit_customer/<str:pk>/', views.editCustomer, name='edit_customer')
]

