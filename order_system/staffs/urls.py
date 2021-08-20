
from django.urls import path, include
from . import views 
from .views import (
    VendorView,
 
)

urlpatterns = [

    path('order-form/', views.createOrder, name='order-form'),
    path('login', views.loginPage, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('register', views.register, name='register'),
    path('order-history/', views.order_history, name='order-history'),
    path('admin-profile', views.admin_dashboard, name='admin-profile'),
    path('admin-cleark', views.admin_cleark, name='admin-clerak'),
    path('chart/', views.chart, name='chart'),
    path('table/', views.table, name='table'),
    path('my-account/<code>/',views.my_account, name='my-account'),
    path('trader-account',views.TraderAccount, name='trade'),
    path('edit-account/<code>/', views.edit_account, name='edit-account'),
    path('wallet/<code>/', views.wallet, name='wallet'),
    path('topup/', views.topUp, name='topup'),
    path('confirm-topup/', views.topup_confirm, name='confirm-topup'),
    path('request-cash/', views.request_cash, name='request-cash'),
    path('confirm-mek-account/', views.confirm_mek_account, name='confirm-mek-account'),
    path('send-money/', views.send_money, name='send-money'),
    path('invest/', views.invest, name='invest'),
    path('ads/', views.Ads, name='ads'),
    path('trans-history/<code>/', views.trans_history, name='trans-history'),
    path('update-client/', views.update_client, name='update-client'),
    path('confirm-code/', views.confirmCode, name='confirm-code'),
    path('add-client/', views.addClient, name='add-client'),
    #path('vendo/account/', views.vendor_account, name='vendor')
    #path('add-vendor/', views.addVendor, name='add-vendor'),
    #path('add-agent/', views.addAgent, name='add-agent'),
    #path('api/data/', views.get_sales_data, name='api-data'),
    #path('api/chart/data/', ChartData.as_view()),
    #path('edit-order/<int:pk>/', views.editOrder, name='edit-order'),
    path('update_order/<str:pk>/',views.updateOrder, name='update_order'), # passing in the primary key of the request objet into the url
    path('confirm-delivey', views.confirm_delivery, name='confirm-delivey'),
    path('contact-us/', views.contact, name='contact'),
    path('save/', views.save_data, name='save'),
    path('delete/', views.delete_contact, name='delete'),
    path('edit/', views.edit_contact, name='edit'),
]
