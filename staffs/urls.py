
from django.urls import path, include
from . import views 



urlpatterns = [
	path('login', views.loginPage, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('register', views.register, name='register'),
    path('profile/', views.user_dashboard, name='profile'),
    path('chart/', views.chart, name='chart'),
    path('table/', views.table, name='table'),
]