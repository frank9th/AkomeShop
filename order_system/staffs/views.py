from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, allowed_users, admin_only  
from django.db.models import Avg, Count, Min, Sum
from django.views.generic import TemplateView, ListView
from .models import *
from .views_snippets import * 
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
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from store.signal_file import *
#from django.views.decorators.csrf import csrf_exempt

t = datetime.datetime.now()
d = datetime.datetime.now()

#datetime.today().strftime('%Y-%m-%d')

time = t.strftime("%X")
date = d.strftime('%Y-%m-%d')




# Create your views here.

def create_slug():
	return ''.join(random.choices(string.ascii_lowercase, k=5))

def create_unique_code():
	return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

def create_trans_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))

def create_funding_code():
	return ''.join(random.choices(string.digits, k=5))


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
				itemid = request.POST.get('itemid')
				name = request.POST['name']
				price = request.POST['price']
				description = request.POST['description']
				cathegory = request.POST['cathegory']
				slug = name + create_slug() 

				create_order = Item(
						title= name,
						price = price,
						category = cathegory,
						description = description,
						slug = slug, 
						)
				create_order.save()
				add_to_cart(request, slug=slug)
		
				con = Item.objects.values()
				print(con)
				item_data = list(con)

				#return JsonResponse({'status':'Save', 'item_data':item_data})

			#else:
				#return JsonResponse({'status':0})

				'''
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
				'''

	except ObjectDoesNotExist:
		
		messages.warning(request, "You do not have an active order")
        #return redirect("/")

	context= {
		'form':form, 
		'object':order
		}
	return render(request, 'order_form.html', context)


# client detail page 
def my_account(request, code):
	client = UserProfile.objects.get(client_code=code)
	orders = client.order_set.all()
	total_order = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()
	out_delivery = orders.filter(status='Out for Delivery').count()
	context= {'client': client, 'orders': orders, 
	'total_order': total_order, 'delivered': delivered, 'pending': pending, 
	'out_delivery':out_delivery }
	return render(request, 'dashboard/page-user.html', context)


def edit_account(request, code):
	client = UserProfile.objects.get(client_code=code)
	form = AccountForm(instance=client)
	if request.method == 'POST':
		form = AccountForm(request.POST , instance=client) 
		if form.is_valid():
			form.save()

	context ={
	'form':form,
	'client':client
	}
	return render (request, 'dashboard/edit-account.html', context)


# wallet page and function 
def wallet(request, code):
	client = UserProfile.objects.get(client_code=code)
	bank = UserAccount.objects.get(user=client.user)
	form = WalletForm(instance=bank)
	if request.method == 'POST':
		form = WalletForm(request.POST , instance=bank) 
		if form.is_valid():
			form.save()
			messages.success(request, "Your Account Details was added successfully!")
		else:
			messages.warning(request, "Your Account details as been updated")

	context = {
	'bank':bank,
	'client':client,
	'form':form,
	'tform':TopUpForm(),
	'wform': TransForm(),
	'sform': SavForm(),
	'sendform':SendMoneyForm(),
	'accnform':ConfirmAccountForm(),
	}
	return render (request, 'dashboard/wallet.html', context)



# top up funds function 
def topUp(request):
	if request.method == "POST":
		acctUserid = request.POST.get('actUser')
		payment = request.POST.get('pay')
		amount = request.POST.get('amount')
		userAcc = UserAccount.objects.get(id=acctUserid)

		'''
		# TODO: if the top up is cash;
		create a refrenfe code and store the request in a request model
		once the code is confirmed, the funds should be sent to the users 
		account and deleted from the ref table. 

		'''
		if payment == 'C':
			fund = TopupFund(
				pay_type=payment,
				amount = amount,
				date=date ,
				time=time, 
				ref_code = create_funding_code(),
				)
			fund.reciever = userAcc
			fund.save()
			return JsonResponse({'status':'Save', 'pending_fund':amount, 'pay_type':payment})

			print("successfully funded account. new balance will reflect in approximately 20min.")

		if payment == 'CD':
			
			print("pls wait while the system redirect you to complet the transaction ")
			return JsonResponse({'status':0, 'pending_fund':amount, 'pay_type':payment})
		if payment == 'U':

			print("Pay into the below account to complect topUp")
			return JsonResponse({'status':1, 'pending_fund':amount, 'pay_type':payment})
		

		return JsonResponse( { 'status':'ok'})

''' request cash out functions '''
def request_cash(request):
	if request.method == "POST":
			acctUserid = request.POST.get('actUser')
			name = request.POST.get('name')
			account = request.POST.get('account_name')
			amount = request.POST.get('amount')
			note = request.POST.get('note')
			userAcc = UserAccount.objects.get(account_name=name)
			userBal = userAcc.wallet_balance
			# converting the form field amount to float 
			cash = float(amount)

			if (userBal > cash):
				new_balance = userBal - cash
				userAcc.wallet_balance = new_balance
				userAcc.save()
				trans = Transaction(
					transaction_type= 'W',
					date= date ,
					time= time,
					amount = cash,
					note = note, 
					ref_code = create_trans_code(),
					)
				trans.account = userAcc
				trans.save()
				return JsonResponse({'status':'Save', 'wallet_balance':new_balance})

			elif (userBal < cash ):
				return JsonResponse({'status':1, 'wallet_balance':userBal})

			elif (userBal <= cash ):
				return JsonResponse({'status':2, 'wallet_balance':userBal})

			else:
				return JsonResponse({'status':0, })

# send money to other account function 
def confirm_mek_account(request):
	if request.method == "POST":
		account_type = request.POST.get('account_type')
		sender = request.POST.get('sender')
		account_number = request.POST.get('reciever_account')
		senderAcc = UserAccount.objects.get(id=sender)	


		# checking if its mek account to get the account number 
		if account_type == 'Mek':
			try:
				rec_account = UserProfile.objects.get(client_code=account_number)
				rec_data = UserAccount.objects.get(user=rec_account.user)
				response = rec_account.first_name + ' ' + rec_account.last_name
				bnk = "Mek Wallet"
				return JsonResponse({'status':'True',
				 'response':response,
				 'bank':bnk, 'number':account_number, 
				 'acc_type': account_type})
				
				#print(response)
				print(rec_data.wallet_balance)


				print(account_type)
					

			except Exception as e:
				return JsonResponse({'status':100 })
			
		if account_type == 'Other':
			print("sending to other bank ")
			return JsonResponse({'status':0 })


	return JsonResponse( { 'status': 50})



def send_money(request):
	if request.method == "POST":
		account_type = request.POST.get('account_type')
		sender = request.POST.get('sender')
		amount = request.POST.get('amount')
		bank = request.POST.get('bank')
		account_number = request.POST.get('account_num')
		senderAcc = UserAccount.objects.get(id=sender)	
		senderBal = senderAcc.wallet_balance

		# checking if its mek account to get the account number 
		if account_type == 'Mek':
			rec_account = UserProfile.objects.get(client_code=account_number)
			rec_data = UserAccount.objects.get(user=rec_account.user)
			#print(rec_account)
			#print(rec_data)
			send_note = "Transfered to " + str(rec_data)  
			rec_note = "Recieved Funds from  " + str(senderAcc)

			recBal = rec_data.wallet_balance
			cash = float(amount)
			low_cash = float(300)


			# Checking Senders Account and deductin the amount 
		
			if (senderBal <= low_cash ):
				return JsonResponse({'status':300, 'wallet_balance':senderBal})


			elif (senderBal > cash ):
				new_balance = senderBal - cash
				senderAcc.wallet_balance = new_balance
				senderAcc.save()

				# Creating sender's transaction 
				sender_trans = Transaction(
					transaction_type= 'SE',
					date= date ,
					time= time,
					note = send_note,
					amount = cash,
					status= 'Debited',
					ref_code = create_trans_code(),
					)
				sender_trans.account = senderAcc
				sender_trans.save()

				# Creating recievers's transaction 
				rec_new_bal = recBal + cash 
				rec_data.wallet_balance = rec_new_bal
				rec_data.save()

				reciever_trans = Transaction(
					transaction_type= 'T',
					date= date ,
					time= time,
					note= rec_note,
					amount = cash,
					status= 'Credited',
					ref_code = create_trans_code(),
					)
				reciever_trans.account = rec_data
				reciever_trans.save()

				return JsonResponse({'status':200, 'wallet_balance':new_balance, 'reciever_wallet_balance':rec_new_bal})

			elif (senderBal < cash ):
				return JsonResponse({'status':100, 'wallet_balance':senderBal})

			elif (senderBal <= cash ):
				return JsonResponse({'status':350, 'wallet_balance':senderBal})

			else:
				return JsonResponse({'status':0, })

	
		if account_type == 'Other':
			print("sending to other bank ")


	return JsonResponse( { 'status':'ok'})



#Invest money from wallet function 
def invest(request):
	if request.method == "POST":
		acctUserid = request.POST.get('actUser')
		amount = request.POST.get('amount')
		userAcc = UserAccount.objects.get(id=acctUserid)
		userBal = userAcc.wallet_balance
		user_save_Bal = userAcc.sav_balance
			# converting the form field amount to float 
		cash = float(amount)

		if (userBal > cash):
			new_balance = userBal - cash
			new_sav_balance = user_save_Bal + cash
			userAcc.wallet_balance = new_balance
			userAcc.sav_balance = new_sav_balance
			userAcc.save()
			
			trans = Transaction(
				transaction_type= 'Save',
				status= 'Debited',
				date= date ,
				time= time,
				amount = cash,
				ref_code = create_trans_code(),
				)
			trans.account = userAcc
			trans.save()
			
			
			return JsonResponse({'status':'Save', 'wallet_balance':new_balance, 'sav_balance':new_sav_balance})

		elif (userBal < cash ):
			return JsonResponse({'status':1, 'wallet_balance':userBal})

		elif (userBal <= cash ):
			return JsonResponse({'status':2, 'wallet_balance':userBal})

	else:
		return JsonResponse({'status':0, })

def trans_history(request, code):
	client = UserProfile.objects.get(client_code=code)
	bank = UserAccount.objects.get(user=client.user)
	trans = bank.transaction_set.all()
	topup = bank.topupfund_set.all()
	context={
	'topup':topup,
	'client':client,
	'bank':bank,
	'trans':trans,
	}
	return render(request, 'dashboard/trans-history.html', context)
	#return render(request, 'dashboard/ui-notifications.html', context)





# not yet in use. wanted to send data to this views via Ajax
# Edite Contact Details 
def update_client(request):
	try:
		if request.method == "POST":
			id = request.POST.get('userId')
			client = Contact.objects.get(pk=id)
			client_data = { 
				"id":client.id,
			    "title": client.title,
			    "first_name": client.first_name,
			    "last_name": client.last_name,
			    "email": client.email,
			    "phone1": client.phone1,
			    "phone2": client.phone2,
			    "town": client.town,
			    "apartment_address": client.apartment_address,
			    "land_mark": client.land_mark,
			    "client_code": client.client_code,
			    "sex": client.sex,
			    #"user": user,
			    "agent_code": client.agent_code,
			    "bus_account": client.bus_account,
			}
			#client_data.save()
			return JsonResponse(client_data)
		
	except Exception as e:
		raise e


class VendorView(ListView):
	template_name = "dashboard/vendor-dashboard.html"
	model = Vendor
	#model = Vpayment
  

def vendor_account(request, code):
	#item = VendorItem.objects.get(vendor.vendor_code)
	#payment = ''
	try:
		payment = Vendor.objects.get(seller=code)
	except Exception as e:
		pass
		print(payment)
	
	vendor = Vendor.objects.get(vendor_code=code)
	#client = vendor.info
	orders = vendor.order_set.all()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()
	out_delivery = orders.filter(status='Out for Delivery').count()

	total_order = orders.count()

	context= {
	#'item':item,
	#'payment':payment,
	#'client':client,
	'vendor':vendor,
	'orders':orders,
	'total_order':total_order,
	'orders': orders, 
	'total_order': total_order, 
	'delivered': delivered, 
	'pending': pending, 
	'out_delivery':out_delivery
	}
		
	return render(request, 'dashboard/vendor-dashboard.html', context)

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
			return redirect('/')
		else:
			messages.info(request, 'Username or password is incorrect')

	context = {'messages':messages}
	return render(request, 'login.html', context)

#@unauthenticated_user
@admin_only
def register(request):	
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')

			group = Group.objects.get(name='client')
			user.groups.add(group)

			#client_code = create_unique_code()
			messages.success(request, 'Account was created for ' + username )
			#return redirect('my-account/'+client_code)
			return redirect('login')

	elif request.user.is_authenticated:
		if request.method == 'POST':
			user = form.save()
			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')

			group = Group.objects.get(name='staff')
			user.groups.add(group)

			#client_code = create_unique_code()
			messages.success(request, 'Account was created for ' + username + 'with ' + client_code)
			return redirect('my-account/'+client_code)

			

	context = {'form':form}
	return render(request, 'register.html', context)

#User Dasbard View 
@login_required(login_url ='login')
#@admin_only
def order_history(request):
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
	return render(request, 'user_account/order_history.html', context)


def password(request):
	return render(request, 'user_account/password.html',{"title":password})

# This is for the Sales Admin Dashboard 
# AdminDashbod View 
@login_required(login_url ='login')
@admin_only
#@allowed_users('admin')
def admin_dashboard(request):
	#clients = Client.objects.all()
	orders = Order.objects.all()
	total_order = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()
	out_delivery = orders.filter(status='Out for Delivery').count()
	context = {
	'orders':orders,
	'total_order':total_order,
	'delivered':delivered,
	'pending':pending,
	'out_delivery':out_delivery,

	}

	return render(request, 'admin_account/dashboard.html', context)

	

# cleark or CFO dashboard 
def admin_cleark(request):
	form = ConTopUpForm()
	client = request.user.userprofile.client_code
	order = Order.objects.all()
	orders = order.filter(status='Delivered')
	delivered = order.filter(status='Delivered').count()
	context = {
	'form':form,
	'client': client,
	'orders':orders,
	'delivered':delivered,

	}
	return render(request, 'dashboard/cleark-dashboard.html', context)


def logoutUser(request):
	logout(request)
	return redirect('login')

def chart(request):
	return render(request, 'user_account/charts.html',{"title":chart})

def table(request):
	return render(request, 'user_account/tables.html',{"title":table})

"""
TODO: to fix bug on this code:
issues: form still submist even with a wrong id
result: httprespos-codes printed on models id_field 
"""

def updateOrder(request, pk): # passing the primary key into the request views.
	agents = Agent.objects.all()
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
			return redirect('/admin-profile')
	context= {
		'form': form, 
		'agents':agents,
		#'vendors':vendors,
		'orders':orders,

	}
	return render(request, 'admin_account/edit_order.html', context)


def confirmCode(request):
	agent_code = request.POST.get('agent')		
	context={}
	return render(request, 'user_account/add_client.html', context)

def confirm_delivery(request):
	form = DeliveryForm(request.POST or None)
	if form.is_valid():
		ref_code = form.cleaned_data.get('ref_code')
		# Edit the order 
		try:
			all_order = Order.objects.get(status='Out for Delivery')
			order_code = all_order.ref_code[-5:]
			if order_code == ref_code :
				#order = Order.objects.get(ref_code=order_code)
				all_order.status = 'Delivered' 
				all_order.save()
				return JsonResponse('Thanks. It was nice doing business with YOU' , safe=False)
				location.reload()
				#messages.info(request, "Thank you ")
				return redirect('/confirm-delivey')
			else:
				messages.info(request, "Order Code is not correct")
				return redirect('/confirm-delivey')

		except ObjectDoesNotExist:
			messages.info(request, "Order does not exist")
	context={'form':form}
	return render(request, 'delivered_order.html', context)

def contact(request):
	form = ContactForm()
	message = Contact.objects.all()
	context = {
	'form':form,
	'object':message,
	}
	return render(request, 'contact.html', context)


# saving contact details 
def save_data(request):
	if request.method == "POST":
		form = ContactForm(request.POST)
		if form.is_valid():
			messageid = request.POST.get('messageid')
			sender = request.POST['sender']
			phone = request.POST['phone']
			text = request.POST['text']
			if (messageid == '' ):
				contact = Contact(sender=sender, phone=phone, text=text)
			else:
				contact = Contact(id=messageid, sender=sender, phone=phone, text=text)

			contact.save()
			con = Contact.objects.values()
			#order = Order.objects.values()
			#print(order)
			contact_data = list(con)
			return JsonResponse({'status':'Save', 'contact_data':contact_data})

		else:
			return JsonResponse({'status':0})

# Delete Contact Details 
def delete_contact(request):
	if request.method == "POST":
		id = request.POST.get('sid')
		pi = Contact.objects.get(pk=id)
		pi.delete()
		return JsonResponse({'status':1})
	else:
		return JsonResponse({'status':0})

# Edite Contact Details 
def edit_contact(request):
	if request.method == "POST":
		id = request.POST.get('sid')
		contact = Contact.objects.get(pk=id)
		contact_data = {"id":contact.id, "sender":contact.sender, "phone":contact.phone, "text":contact.text}
		return JsonResponse(contact_data)
