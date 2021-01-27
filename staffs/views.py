from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, allowed_users, admin_only  
from .models import *
from django.http import JsonResponse 
import json 
import datetime
from .forms import *
# Create your views here.
from django.contrib import messages

# Create your views here.




@unauthenticated_user
def loginPage(request):
	
	if request.method == 'POST':
		# assigning varables to the username and password field 
		username = request.POST.get('username')
		password = request.POST.get('password')

		#authenticating the fields through django authentication package 

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username or password is incorrect')

	context = {'messages':messages}
	return render(request, 'login.html', context)

@unauthenticated_user
def register(request):
	
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			group = Group.objects.get(name='member')
			user.groups.add(group)
			Customer.objects.create(
				user=user,
				name=user.username,
				)
			
			messages.success(request, 'Account was created for' + username)
			return redirect('login')

	context = {'form':form}
	return render(request, 'register.html', context)



#User Dasbard View 
@login_required(login_url ='login')
#@admin_only
def user_dashboard(request):

	orders = request.user.customer.order_set.all()
	total_order = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()
	out_delivery = orders.filter(status='Out for Delivery').count()
	
	context = {
	'orders': orders, 
	'total_order': total_order,
	'delivered': delivered,
	'pending': pending,
	'out_delivery': out_delivery
	}
	return render(request, 'user_account/user_dashboard.html', context)



def password(request):
	return render(request, 'user_account/password.html',{"title":password})



# AdminDashbod View 
@login_required(login_url ='login')
@admin_only
@allowed_users('admin')
def admin_dashboard(request):
	context = {}
	return render(request, 'admin_account/admin_dashboard.html', context)


def logoutUser(request):
	logout(request)
	return redirect('login')


def chart(request):
	return render(request, 'user_account/charts.html',{"title":chart})

def table(request):
	return render(request, 'user_account/tables.html',{"title":table})
