
from django.urls import path, include
from . import views 
from rest_framework import routers 

router = routers.DefaultRouter()
router.register('api/shop/all/profile', views.AllUserView)
#router.register('api/create/account', views.UserAccount)
router.register('api/shop/vendor/data', views.VendorView)
#router.register('api/shop/order/data', views.OrderView)

app_name = 'shopapi'

urlpatterns = [
	path('', include(router.urls)), 
	path('api/', views.apiOverview, name='api'),
	path('api/profile/', views.AllUserProfile, name='alluser-profile'),
	path('api/profile/<str:code>/', views.SingleUserProfile, name='single-profile'),
	path('api/profile/update/', views.UpdateProfile, name='updete-profile'),

	path('api/shop/order/data/', views.OrderView, name='order-list'),


	path('api/client-detail/<str:pk>/user/', views.ClientDetail, name='client-detail'),
	path('api/add-client/', views.AddClient, name='add-client'),
	path('api/client-update/<str:pk>/user/', views.ClientUpdate, name='update-client'),
	path('api/client-delete/<str:pk>/user/', views.DeleteClient, name='delete-client'),
]
