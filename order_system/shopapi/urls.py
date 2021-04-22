
from django.urls import path, include
from . import views 
from rest_framework import routers 

router = routers.DefaultRouter()
#router.register('api/shop/vpay/data', views.VpayView)
router.register('api/client/data/users', views.ClientView)
router.register('api/shop/vendor/data', views.VendorView)
router.register('api/shop/order/data', views.OrderView)

urlpatterns = [
	path('', include(router.urls)), 
	path('api/', views.apiOverview, name='api'),
	path('api/client-detail/<str:pk>/user/', views.ClientDetail, name='client-detail'),
	path('api/add-client/', views.AddClient, name='add-client'),
	path('api/client-update/<str:pk>/user/', views.ClientUpdate, name='update-client'),
	path('api/client-delete/<str:pk>/user/', views.DeleteClient, name='delete-client'),
]
