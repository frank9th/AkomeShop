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
from store.views import *
from store.models import *
import random 
import string 
from django.contrib import messages



# Create your views here.

def create_slug():
	return ''.join(random.choices(string.ascii_lowercase, k=5))

def create_unique_code():
	return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

def get_client_code(request, code):	
	try:
		client_code = Client.objects.get(client_code=code)
		messages.success(request, "The User is doing Great")
		return client_code 
	except ObjectDoesNotExist:
		#agent_code = {}
		messages.warning(request, "Enter a valid user code ")
		return redirect('/')

def get_agent_code(request, code):	
	try:
		agent_code = Agent.objects.get(agent_code=code)
		messages.success(request, "The Agent is actually well feed")
		return agent_code 
	except ObjectDoesNotExist:
		#agent_code = {}
		messages.warning(request, "Enter a valid agent code ")
		return redirect('/')



@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("store:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("store:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("store:order-summary")



# Create Order 
def createOrder(request):
	user = request.user
	form = OrderForm()
	try:
		order, created = Order.objects.get_or_create(user=user, ordered=False)
		if request.method =='POST':
			#print('Printing post:', request.POST)
			form = OrderForm(request.POST or None) # throwing the post data into the form 
			if form.is_valid(): # performing valid check 
				name = form.cleaned_data.get('name')
				price = form.cleaned_data.get('price')
				cathegory = form.cleaned_data.get('cathegory')
				description = form.cleaned_data.get('description')
				slug = name + create_slug() 

				create_order = Item(
					title= name,
					price = price,
					category = cathegory,
					description = description,
					slug = slug, 
					)
				create_order.save()
				#form.save() # saving the data in the db 
				#slug = form.cleaned_data.get('slug')
				add_to_cart(request, slug=slug)
	except ObjectDoesNotExist:
		
		messages.warning(request, "You do not have an active order")
        #return redirect("/")

	context= {
		'form':form, 
		'object':order
		}
	return render(request, 'order_form.html', context)



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
	orders = request.user.order_set.all()
	item_ordered = orders.filter(ordered=True)
	total_order = item_ordered.count()
	delivered = item_ordered.filter(status='Delivered').count()
	pending = item_ordered.filter(status='Pending').count()
	out_delivery = item_ordered.filter(status='Out for Delivery').count()
	
	context = {
	'orders': item_ordered, 
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
	client = Client.objects.all()
	orders = Order.objects.all()
	total_order = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()
	out_delivery = orders.filter(status='Out for Delivery').count()
	context = {
	'client':client,
	'orders':orders,
	'total_order':total_order,
	'delivered':delivered,
	'pending':pending,
	'out_delivery':out_delivery,

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


	 
	context= {'form': form, 'orders':orders}
	return render(request, 'edit_customer.html', context)

"""
TODO: to fix bug on this code:
issues: form still submist even with a wrong id
result: httprespos-codes printed on models id_field 
"""

def updateOrder(request, pk): # passing the primary key into the request views.
	agents = Agent.objects.all()
	vendors = Vendor.objects.all()
	orders = Order.objects.get(id=pk) # get the pk from the oder objects in the db from models
	form = UpdateOrderForm(instance=orders) # pass the instance into the form so it populate the form 
	# sending the data as post data and redirecting back 
	if request.method =='POST':
		#print('Printing post:', request.POST)
		form = UpdateOrderForm(request.POST, instance=orders) # throwing the post data into the form 
		if form.is_valid(): # performing valid check 
			orders.status = 'Out for Delivery'
			orders.save()
			#form.save() # saving the data in the db

			'''
			#TODO: Send order detail to client,
			# Vendor,
			#supper admin 
			# agent 

			'''
			return redirect('/admin-profile')
	context= {
		'form': form, 
		'agents':agents,
		'vendors':vendors,
		'orders':orders,

	}
	return render(request, 'admin_account/edit_order.html', context)


def confirmCode(request):
	agent_code = request.POST.get('agent')	
	
	context={}
	return render(request, 'user_account/add_client.html', context)


def addClient(request):
	code = request.POST.get('code')
	client = get_client_code(request, code)
	form = AddClientForm( request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			try:

				title= form.cleaned_data.get('title')
				full_name=form.cleaned_data.get('full_name')
				phone1=form.cleaned_data.get('phone1')
				phone2=form.cleaned_data.get('phone2')
				email= form.cleaned_data.get('email')
				agent_code= form.cleaned_data.get('agent_code')
				land_mark= form.cleaned_data.get('land_mark')
				town = form.cleaned_data.get('town')
				sex = form.cleaned_data.get('sex')
				apartment_address=form.cleaned_data.get('apartment_address')
				client_code = create_unique_code()
			
				client_details= Client(
					title= title,
					full_name = full_name,
					email = email,
					phone1 = phone1,
					phone2 = phone2,
					town = town,
					apartment_address = apartment_address,
					client_code = client_code,
					agent_code = agent_code
					)	

				client_details.save()
				messages.success(request, title  +  full_name +  " registerd successully client's code is: " + client_code )
				return redirect('/profile')
				# TODO: Send Code as SMS TO CLIENT 
			except ObjectDoesNotExist:
				messages.info(request, "The Client already exist ")				
	context={
	'form':form, 
	'client':client,
	#'agent_form':CodeForm(),
	}
	return render(request, 'user_account/add_client.html', context)

def addVendor(request):
	code = request.POST.get('code')
	client = get_client_code(request, code)
	#agent = get_agent_code(request, code)

	try:
		clientId = Client.objects.get(id=request.POST.get('clientId'))
		agentId = Agent.objects.get(id=request.POST.get('agentId'))
	except Exception as e:
		pass

	form = AddVendorForm(request.POST or None )
	if request.method == 'POST':
		if form.is_valid():
			business_name = form.cleaned_data.get('business_name')
			product_name = form.cleaned_data.get('product_name')
			goods = form.cleaned_data.get('goods')
			services = form.cleaned_data.get('services')
			skill = form.cleaned_data.get('skill')
			agent_code = form.cleaned_data.get('agent_code')
			try:
				agent = Agent.objects.get(id=request.POST.get(agent_code))
			except Exception as e:
				pass

			vendor_code = create_unique_code()
			vendor_details = Vendor(
				info = clientId,
				business_name = business_name, 
				product_name = product_name, 
				goods = goods, 
				services = services, 
				skill = skill, 
				vendor_code = vendor_code,
				#agent_code= agent,
				)
			vendor_details.save()
			messages.success(request, " registerd successully vendor's code is:" + vendor_code )
			
			# TODO: Send Code as SMS TO VENDOR 
			return redirect('/profile')

	context={'form':form, 
	'client':client,
	#'agent': agent
	}
	return render(request, 'user_account/add_vendor.html', context)

def addAgent(request):
	code = request.POST.get('code')
	client = get_client_code(request, code)


	form = AddAgentForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			bike = form.cleaned_data.get('bike')
			keke = form.cleaned_data.get('keke')
			car = form.cleaned_data.get('car')
			agent_type = form.cleaned_data.get('agent_type')
			agent_code = create_unique_code()
			#codebox = Codebox(code=agent_code, name=full_name)
			#codebox.save()
			agent_details = agent
			agent_details = Agent(
				bike = bike, 
				keke = keke,
				car = car,
				agent_type= agent_type,
				agent_code=agent_code
				)
			#agent_details.agent_code = codebox
			agent_details.save()
			messages.success( request, " Agent added succesfully. Agent code:" + agent_code )
			# TODO: SEND CODE 
			return redirect('/profile')

	context={'form':form, 'client':client}
	return render(request, 'user_account/add_agent.html', context)



def confirm_delivery(request):
	form = DeliveryForm(request.POST or None)
	if form.is_valid():
		ref_code = form.cleaned_data.get('ref_code')
		# Edit the order 
		try:
			order = Order.objects.get(ref_code=ref_code)
			order.status = 'Delivered' 
			order.save()

			return JsonResponse('Thanks. It was nice doing business with YOU' , safe=False)
			location.reload()
			#messages.info(request, "Thank you ")
			return redirect('/confirm-delivey')

		except ObjectDoesNotExist:
			messages.info(request, "Order does not exist")
	context={'form':form}
	return render(request, 'store/delivered_order.html', context)
	
