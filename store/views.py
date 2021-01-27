
from django.shortcuts import render, redirect 
from django.forms import inlineformset_factory
from .models import *
from .forms import * 
from staffs.forms import *
# Create your views here.

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
	return render(request, 'home.html', context)

# for customer profile 
def customer(request, pk):
	customer = Customer.objects.get(id=pk)

	orders= customer.order_set_all()
	order_count = orders.count()

	context = {'customer':customer, 'orders': orders, 'order_count':order_count}
	return render(request, 'account/customer.html', context)

# cart page 

def cart(request):
	context= {}
	return render(request, 'store/cart.html', context)

#Checkout 
def checkout(request):
	form= CreataOrderForm()
	#form = OrderForm()
	customer = request.user
	if request.method =='POST':
		#print('Printing post:', request.POST)
		form = OrderForm(request.POST, instance=customer) # throwing the post data into the form 
		if form.is_valid(): # performing valid check 
			form.save() # saving the data in the db 
			return redirect('checkout')

	context= {'form':form}
	return render(request, 'store/checkout.html', context)

#Home page- Product list page  
def homePage(request):
	item = Product.objects.all()
	context= {'item':item}
	return render(request, 'store/home-page.html', context)


#Product view page  
def product(request):
	context= {}
	return render(request, 'store/product-page.html', context)





# Create Order 
def createOrder(request):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status', 'customer'))
	#customer = Customer.objects.get(id=pk)
	formset = OrderFormSet()
	form = OrderForm()
	if request.method =='POST':
		#print('Printing post:', request.POST)
		form = OrderForm(request.POST) # throwing the post data into the form 
		if form.is_valid(): # performing valid check 
			form.save() # saving the data in the db 
			return redirect('/')
	context= {'formset': formset, 'form':form}
	return render(request, 'store/order_form.html', context)


# Update customers order-

def updateOrder(request, pk): # passing the primary key into the request views.

	order = Order.objects.get(id=pk) # get the pk from the oder objects in the db from models
	form = OrderForm(instance=order) # pass the instance into the form so it populate the form 

	# sending the data as post data and redirecting back 
	if request.method =='POST':
		#print('Printing post:', request.POST)
		form = OrderForm(request.POST, instance=order) # throwing the post data into the form 
		if form.is_valid(): # performing valid check 
			form.save() # saving the data in the db 
			return redirect('/')

	context= {'form': form}
	return render(request, 'store/order_form.html', context)


# Delete Item 
def delete_item(request, pk):
	item = Order.objects.get(id=pk)
	if request.method =='POST':
		#print('Printing post:', request.POST)
			item.delete() # saving the data in the db 
			return redirect('/')


	context= {'item':item}
	return render(request, 'store/delete.html', context)

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