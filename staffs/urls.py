
from django.urls import path, include
from . import views 



urlpatterns = [
	path('login', views.loginPage, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('register', views.register, name='register'),
    path('profile/', views.user_dashboard, name='profile'),
    path('customer/<str:pk>/', views.customer, name='customer'),
    path('admin-profile', views.admin_dashboard, name='admin-profile'),
    path('chart/', views.chart, name='chart'),
    path('table/', views.table, name='table'),
    path('home-sales',views.salesHome, name='home-sales'),
    #path('add_customer', views.addCustomer, name='add_customer'),
	#path('edit_customer/<str:pk>/', views.editCustomer, name='edit_customer'),
	path('confirm-code/', views.confirmCode, name='confirm-code'),
    path('add-client/', views.addClient, name='add-client'),
	path('add-vendor/', views.addVendor, name='add-vendor'),
	path('add-agent/', views.addAgent, name='add-agent'),
    #path('edit-order/<int:pk>/', views.editOrder, name='edit-order'),
    path('update_order/<str:pk>/',views.updateOrder, name='update_order'), # passing in the primary key of the request objet into the url
    path('confirm-delivey', views.confirm_delivery, name='confirm-delivey'),
]
