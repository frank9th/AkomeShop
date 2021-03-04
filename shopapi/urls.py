
from django.urls import path, include
from . import views 
from rest_framework import routers 

router = routers.DefaultRouter()
router.register('api/shop/vpay/data', views.VpayView)
router.register('api/shop/client/data', views.ClientView)
router.register('api/shop/vendor/data', views.VendorView)

urlpatterns = [
	path('', include(router.urls)), 
]
