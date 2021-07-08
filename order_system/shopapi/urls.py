
from django.urls import path, include
from . import views 
#from .views import ListUsers, CustomAuthToken, ExampleView, 
from .views import *
from rest_framework import routers 



router = routers.DefaultRouter()
router.register('api/shop/all/profile', views.AllUserView)
#router.register('api/create/account', views.UserAccount)
router.register('api/vendor/data', views.VendorView)
router.register('api/product/data', views.ProductView)
#router.register('api/shop/order/data', views.OrderView)

app_name = 'shopapi'

urlpatterns = [
	path('api/auth/user', ExampleView.as_view()),
	path('api/rest-auth/', include('rest_auth.urls')),
	path('api/rest-auth/registration/', include('rest_auth.registration.urls')),
	path('api/auth', include('djoser.urls.authtoken')),
	path('api/auth/user', include('rest_framework.urls', namespace='rest_framework')),
	path('api/auth/mek/', include('djoser.urls')),
	path('api/rest-auth/facebook/', FacebookLogin.as_view(), name='fb_login'),

	path('api/create-product/', views.AddProduct, name='create_produt'),




	path('api/token/auth/', CustomAuthToken.as_view()),
	path('api/users/', ListUsers.as_view()),
	path('', include(router.urls)), 
	path('api/', views.apiOverview, name='api'),
	path('api/profile/', views.AllUserProfile, name='alluser-profile'),
	path('api/profile/<str:code>/', views.SingleUserProfile, name='single-profile'),
	path('api/profile/update/<str:code>/', views.UpdateProfile, name='updete-profile'),
	path('api/shop/order/data/', views.OrderView, name='order-list'),
	path('api/profile/account/<str:pk>/', views.UserAccountDetails, name='account-details'),


	path('api/client-detail/<str:pk>/user/', views.ClientDetail, name='client-detail'),
	path('api/add-client/', views.AddClient, name='add-client'),
	path('api/client-update/<str:pk>/user/', views.ClientUpdate, name='update-client'),
	path('api/client-delete/<str:pk>/user/', views.DeleteClient, name='delete-client'),
]

