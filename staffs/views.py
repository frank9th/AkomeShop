from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, allowed_users, admin_only  
from .models import *
import sys
import requests
from django.http import JsonResponse 
import json 
import datetime
from .forms import *
from store import *
from store.views import *
from store.models import *
import random 
import string 
from django.contrib import messages

# Create your views here.

def create_unique_id():
	return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))



def get_agent_id(request, code):
	try:
		agent_code = Agent.objects.get(agent_id=code)
		return agent_code 
	except ObjectDoesNotExist:
		messages.info(request, "This Agent does not exist")
		return redirect('/add_client')


# home view 
def salesHome(request):
	#orders = Order.objects.all()
	orders = request.user.customer.order_set.all()
	customer = Customer.objects.all()
	total_order = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()
	out_delivery = orders.filter(status='Out for Delivery').count()

	context= {'customer': customer, 'orders': orders, 
	'total_order': total_order, 'delivered': delivered, 'pending': pending, 
	'out_delivery':out_delivery }
	return render(request, 'user_account/home_sales.html', context)


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
			email = form.cleaned_data.get('email')

			group = Group.objects.get(name='staff')
			user.groups.add(group)
			Customer.objects.create(
				user=user,
				name=user.username,
				email=user.email,
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


# for customer profile 
def customer(request, pk):
	customer = Customer.objects.get(id=pk)
	orders= customer.order()
	order_count = orders.count()

	context = {'customer':customer, 'orders': orders, 'order_count':order_count}
	return render(request, 'account/customer.html', context)


def password(request):
	return render(request, 'user_account/password.html',{"title":password})


# AdminDashbod View 
@login_required(login_url ='login')
@admin_only
#@allowed_users('admin')
def admin_dashboard(request):
	customer = Customer.objects.all()
	context = {
	'customer':customer
	}
	return render(request, 'admin_account/dashboard.html', context)


def logoutUser(request):
	logout(request)
	return redirect('login')

def chart(request):
	return render(request, 'user_account/charts.html',{"title":chart})

def table(request):
	return render(request, 'user_account/tables.html',{"title":table})

# Add customer
def addCustomer(request):
	form = addCustomerForm()
	if request.method == 'POST':
		#print('Printing post:', request.POST)
		form = addCustomerForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')


	context= {'form':form}
	return render(request, 'add_customer.html', context)

# Edit Customer- not yet working
def editCustomer(request, pk): 
	customer = Customer.objects.get(id=pk) 
	form = addCustomerForm(instance=customer) 
	if request.method =='POST':
		form = addCustomerForm(request.POST , instance=customer) 
		if form.is_valid(): # performing valid check 
			form.save() # saving the data in the db 
			return redirect('home')


	 
	context= {'form': form}
	return render(request, 'edit_customer.html', context)

"""
TODO: to fix bug on this code:
issues: form still submist even with a wrong id
result: httprespos-codes printed on models id_field 
"""
def addClient(request):
	form = AddClientForm( request.POST or None)
	if request.method == 'POST':

		if form.is_valid():
			try:
				title= form.cleaned_data.get('title')
				full_name=form.cleaned_data.get('full_name')
				phone=form.cleaned_data.get('phone')
				email= form.cleaned_data.get('email')
				land_mark= form.cleaned_data.get('land_mark')
				town = form.cleaned_data.get('town')
				apartment_address=form.cleaned_data.get('apartment_address')
				client_id = create_unique_id()
				agent_id = form.cleaned_data.get('agent_id')

				agent =get_agent_id(request, agent_id)

				client_details= Client(
					title= title,
					full_name = full_name,
					email = email,
					phone = phone,
					town = town,
					address = apartment_address,
					client_id = client_id,
					agent_id = agent,
					)
				
				client_details.save()
				messages.success(request, title  +  full_name +  " registerd successully client's code is: " + client_id )
				# TODO: Send Code as SMS TO CLIENT 
			except ObjectDoesNotExist:
				messages.info(request, "The Client already exist ")		
			
	context={'form':form}
	return render(request, 'user_account/add_client.html', context)

def addVendor(request):
	form = AddVendorForm(request.POST or None )
	if request.method == 'POST':
		if form.is_valid():
			first_name = form.cleaned_data.get('first_name')
			last_name = form.cleaned_data.get('last_name')
			sex = form.cleaned_data.get('sex')
			email = form.cleaned_data.get('email')
			apartment_address = form.cleaned_data.get('apartment_address')
			street_address = form.cleaned_data.get('street_address')
			phone1 = form.cleaned_data.get('phone1')
			phone2 = form.cleaned_data.get('phone2')
			business_name = form.cleaned_data.get('business_name')
			product_name = form.cleaned_data.get('product_name')
			goods = form.cleaned_data.get('goods')
			services = form.cleaned_data.get('services')
			skill = form.cleaned_data.get('skill')

			vendor_id = create_unique_id()

			vendor_details = Vendor(
				first_name = first_name,
				last_name = last_name, 
				sex = sex, 
				email = email, 
				apartment_address = apartment_address, 
				street_address = street_address, 
				phone1 = phone1, 
				phone2 = phone2, 
				business_name = business_name, 
				product_name = product_name, 
				goods = goods, 
				services = services, 
				skill = skill, 
				vendor_id = vendor_id,
				)
			vendor_details.save()
			messages.success(request, first_name  +  last_name +  " registerd successully vendor's code is:" + vendor_id )
			# TODO: Send Code as SMS TO VENDOR 
			return redirect('/profile')

	context={'form':form}
	return render(request, 'user_account/add_vendor.html', context)

def addAgent(request):
	form = AddAgentForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			full_name = form.cleaned_data.get('full_name')
			email = form.cleaned_data.get('email')
			phone1 = form.cleaned_data.get('phone1')
			phone2 = form.cleaned_data.get('phone2')
			town = form.cleaned_data.get('town')
			address = form.cleaned_data.get('address')
			bike = form.cleaned_data.get('bike')
			keke = form.cleaned_data.get('keke')
			car = form.cleaned_data.get('car')
			agent_type = form.cleaned_data.get('agent_type')


			agent_id = create_unique_id()
			print(agent_type)

			agent_details = Agent(

				full_name= full_name,
				email = email,
				phone1 = phone1,
				phone2 = phone2,
				town =town, 
				address = address,
				bike = bike, 
				keke = keke,
				car = car,
				agent_type= agent_type,
				agent_id = agent_id
				)
			agent_details.save()
			messages.success( request, " Agent added succesfully. Agent Id:" + agent_id )
			# TODO: SEND CODE 
			return redirect('/profile')

	context={'form':form}
	return render(request, 'user_account/add_agent.html', context)