

from django.conf import settings 
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.forms import inlineformset_factory
from django.views.generic import ListView, DetailView, View
from .models import *
from .forms import * 
from staffs.forms import *
from django.utils import timezone
import random 
import string 
import stripe


stripe.api_key = settings.STRIPE_API_KEY

def create_ref_code():
	return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))

 # Uses the same API Key.
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

# This is the cart page to enter customer detail page nd checkout 
def cart(request):
	form = CheckOutForm(request.POST or None)
	try:
		customer = request.user.customer
		order = Order.objects.get(is_ordered=False, customer=customer)
		item = OrderItem.objects.filter(customer=customer, is_ordered=False)
		#print(item)

		if form.is_valid():
			# Geting the specified fields 
			client_name = form.cleaned_data.get('client_name')
			street_address = form.cleaned_data.get('street_address')
			apartment_address = form.cleaned_data.get('apartment_address')
			country = form.cleaned_data.get('country')
			zip_code = form.cleaned_data.get('zip_code')
			

			# TODO- ADD FUNCTIONALITY TO THIS FIELDS 
			#same_shipping_address = form.cleaned_data.get('same_shipping_address')
			#save_info = form.cleaned_data.get('save_info')
			payment_option = form.cleaned_data.get('payment_option')

			# passing the required fields into the model and assigning varable to the fields 
			billing_address = BillingAddress(
				customer = request.user.customer,
				client_name = client_name,
				street_address = street_address,
				apartment_address = apartment_address,
				country = country,
				zip_code = zip_code
				)
			billing_address.save()
			#assigning the billing address to the order 
			order.billing_address = billing_address
			order.save()
			# TODO: Add redirect to the selected payment option 
			#return redirect('home')
			if payment_option == 'S':
				return redirect('payment', payment_option='stripe')

			elif payment_option == 'P':
				return redirect('payment', payment_option='paypal')
			else:
				payment_option =='PD'
				order.is_ordered = True
				order.amount = 200
				order.ref_code =  create_ref_code()
				order.save()
				#updating the item in cart to ordered
				order_items= OrderItem.objects.all()
				order_items.update(is_ordered=True)
				for item in order_items:
					item.save()
				messages.success(request, "Your order was succesfull ")
				return redirect('home')

	except ObjectDoesNotExist:
		messages.error(request, "You do not have an active order")
	#return render(request, 'home')

	context= {'form':form, 'item':item, 'couponform':CouponForm(), 'order':order}
	#messages.warning(request, "Failed checkout")
	return render(request, 'store/checkout-page.html', context)



def paymentPage(request, payment_option):
	customer = request.user.customer
	order = Order.objects.get(customer=customer, is_ordered=False)
	hand_coded_amount = 100  # this is because the total amout is not yet working 
	amount = int(order.get_total() * 100)
	token = request.POST.get('stripeToken')
	if order.billing_address:
		try:
			charge = stripe.Charge.retrieve(
			  "ch_1IEsVz2eZvKYlo2CXoYPSpIP",
			  api_key="sk_test_4eC39HqLyjWDarjtT1zdp7dc",
			  amount = hand_coded_amount * 100, 
			  currency = "NGN",
			  source = token,
			  description = "charge for Jenny.rosen@example.com"
			)
			  # create payment 
			payment = Payment()
			payment.stripe_charge_id = charge['id'] # or use charge.id to access the stripe generated id from the api call above.
			payment.customer = customer 
			payment.amount = hand_coded_amount
			payment.save()
			# assign payment to the order. 
			order.is_ordered = True
			order.payment = hand_coded_amount
			# TODO- assign refrence code 
			order.ref_code =  create_ref_code()
			order.save()
			messages.success(request, "Yoour order was succesfull ")
			return redirect('home')
			

		except stripe.error.CardError as e:
			messages.error(request, "Invalid card details")
		  # Since it's a decline, stripe.error.CardError will be caught
		except stripe.error.RateLimitError as e:
			messages.error(request, "time limit reached ")
		  # Too many requests made to the API too quickly
		except stripe.error.InvalidRequestError as e:
			messages.error(request, "Invalid paramiters")
		  # Invalid parameters were supplied to Stripe's API
		except stripe.error.AuthenticationError as e:
			messages.error(request, "not Authenticated")

		  # Authentication with Stripe's API failed
		  # (maybe you changed API keys recently)

		except stripe.error.APIConnectionError as e:
			messages.error(request, "Check your network connection")
		  # Network communication with Stripe failed
		except stripe.error.StripeError as e:
			messages.error(request, "Something went wrong, you were not charged ")
		  # Display a very generic error to the user, and maybe send
		  # yourself an email
		except Exception as e:
			messages.error(request, "Serious error, we have been notified")
			# send email to our self. 
		  # Something else happened, completely unrelated to Stripe

		context= {'order':order, }
		return render(request, 'store/payment.html', context)
	else:
		messages.warning(request, "You have not added a billing address")
		return redirect("/cart/")
		



#Checkout This is the cart page with the order 
def checkout(request):
	form= CreataOrderForm()
	couponForm = CouponForm()
	#form = OrderForm()
	customer = request.user
	if request.method =='POST':
		#print('Printing post:', request.POST)
		form = OrderForm(request.POST, instance=customer) # throwing the post data into the form 
		if form.is_valid(): # performing valid check 
			form.save() # saving the data in the db 
			return redirect('checkout')

	context= {'form':form, 'couponForm':couponForm}
	return render(request, 'store/checkout.html', context)

#Home page- Product list page  
def homePage(request):
	item = Product.objects.all()
	context= {'item':item}
	return render(request, 'store/home-page.html', context)


#Product detail page 
def productDetailView(request, slug):
	product = Product.objects.get(slug=slug)
	context = {'product':product}

	#return render(request, 'store/store.html',  context)
	return render(request, 'store/product-page.html',  context)

@login_required 
def add_to_cart(request, slug):
	#grab the item by the slug 
	customer = request.user.customer
	item = get_object_or_404(Product, slug=slug)
	# create that item in OrderItem 
	order_item, created = OrderItem.objects.get_or_create(item=item, customer=customer, is_ordered=False)
	order_qs = Order.objects.filter(customer=customer, is_ordered=False)
	if order_qs.exists():
		order = order_qs[0]
		# check if item is in order 
		if order.product.filter(item__slug=item.slug).exists():
			order_item.quantity += 1
			order_item.save()
			messages.info(request, "This item quantity was updated")

		else:
			messages.info(request, "This item was added to your cart")
			order.product.add(order_item)
	else:
		date_created = timezone.now()
		order = Order.objects.create(customer=customer, date_created=date_created)
		order.product.add(order_item)
		messages.info(request, "This item was added to your cart")
	return redirect("order-summary")



@login_required
def remove_form_cart(request, slug):
	#grab the item by the slug 
	customer = request.user.customer
	item = get_object_or_404(Product, slug=slug)
	# create that item in OrderItem 
	order_item, created = OrderItem.objects.get_or_create(item=item, customer=customer, is_ordered=False)
	order_qs = Order.objects.filter(customer=customer, is_ordered=False)
	if order_qs.exists():
		order = order_qs[0]
		# check if item is in order 
		if order.product.filter(item__slug=item.slug).exists():
			order_item = OrderItem.objects.filter(item=item, 
				customer=customer, is_ordered=False)[0]
			order_item.delete()
			messages.info(request, "This item was removed from your cart")
			return redirect("order-summary")
		else:
			# add a message; order does not contain dis order
			messages.info(request, "This item was not in your cart")
			return redirect("order-summary")


	else:
		messages.info(request, "You don't have an active order ")
		return redirect("order-summary")

@login_required
def OrderSummary(request):
	try:
		customer = request.user.customer
		item = OrderItem.objects.filter(customer=customer, is_ordered=False)
		order ={'get_total':0, 'get_cart_items':0, 'shipping':False}
		context={'item':item, 'order':order}
		return render(request, 'store/order_summary.html', context)

		#item = OrderItem.objects.filter(is_ordered=False, customer=customer)
		#print(item)
	except ObjectDoesNotExist:
		messages.error(request, "You do not have an active order")
		return redirect("/")



@login_required
def OrderSummaryBE(request):
	try:
		customer = request.user.customer
		item = OrderItem.objects.filter(customer=customer, is_ordered=False)
		order ={'get_total':0, 'get_cart_items':0, 'shipping':False}
		context={'item':item, 'order':order}
		return render(request, 'store/order_form.html', context)
	except ObjectDoesNotExist:
		messages.error(request, "You do not have an active order")
		return redirect("/")
		
	



@login_required
def remove_single_item(request, slug):
	#grab the item by the slug 
	customer = request.user.customer
	item = get_object_or_404(Product, slug=slug)
	# create that item in OrderItem 
	order_item, created = OrderItem.objects.get_or_create(item=item, customer=customer, is_ordered=False)
	order_qs = Order.objects.filter(customer=customer, is_ordered=False)
	if order_qs.exists():
		order = order_qs[0]
		# check if item is in order 
		if order.product.filter(item__slug=item.slug).exists():
			order_item = OrderItem.objects.filter(item=item, 
				customer=customer, is_ordered=False)[0]

			order_item.quantity -= 1
			order_item.save()
			if order_item.quantity <= 0:
				order_item.delete()
			messages.info(request, "This item quantity was updated")
			return redirect("order-summary")
		else:
			# add a message; order does not contain dis order
			messages.info(request, "This item was not in your cart")
			return redirect("product")

	else:
		messages.info(request, "You don't have an active order ")
		return redirect("product")



# Create Order 
def createOrder(request):
	#OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status', 'customer'))
	#customer = Customer.objects.get(id=pk)
	user = request.user
	customer = request.user.customer
	item = OrderItem.objects.filter(customer=customer, is_ordered=False)
	order ={'get_total':0, 'get_cart_items':0, 'shipping':False}
	form = OrderForm()
	if request.method =='POST':
		#print('Printing post:', request.POST)
		form = OrderForm(request.POST) # throwing the post data into the form 
		if form.is_valid(): # performing valid check 
			form.save() # saving the data in the db 
			slug = form.cleaned_data.get('slug')
			add_to_cart(request, slug=slug)
	context= {'form':form, 'item':item, 'order':order}
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


# adding copon code 
def get_coupon(request):

	try:
		coupon = Coupon.objects.get()
		return coupon 
	except ObjectDoesNotExist:
		messages.info(request, "This coupon does not exist")
		return redirect("store/checkout-page.html")

	

# adding copon code 
def add_coupon(request):
	if request.method == "POST":
		form = CouponForm(request.POST or None)
		if form.is_valid():
			try:
				code = form.cleaned_data.get('code')
				customer = request.user.customer
				order.coupon = get_coupon(code)
				order.save()
				messages.success(request, "coupon added succesfully")
				return redirect("checkout")

			except ObjectDoesNotExist:
				messages.info(request, "You do not have an active order")
				return redirect("store/checkout-page.html")
	# TODO: raise Error
	return None

def RequestRefund(request):
		form = RefundForm(request.POST)
		if form.is_valid():
			ref_code = form.cleaned_data.get('ref_code')
			message = form.cleaned_data.get('message')
			email = form.cleaned_data.get('email')
			# Edit the order 
			try:
				order = Order.objects.get(ref_code=ref_code)
				order.refund_requested = True 
				order.save()
			# define refund model 
				refund = Refund()
				refund.order = order
				refund.reason = message 
				refund.save()

				messages.info(request, "Your request have been submited")
				return redirect("request-refund")

			except ObjectDoesNotExist:
				messages.info(request, "Order does not exist")
		context={
		'form':form
		}

		return render(request, "store/request_refund.html", context)
