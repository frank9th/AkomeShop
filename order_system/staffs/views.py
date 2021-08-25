from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import Group
from .decorators import *
from django.db.models import Avg, Count, Min, Sum
from django.views.generic import TemplateView, ListView
from .models import *
from .views_snippets import * 
import sys
import requests
from django.http import JsonResponse 
import json 
import datetime
from dateutil.relativedelta import relativedelta
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
from decouple import config 
from django.conf import settings
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
	return ''.join(random.choices(string.digits, k=10))

def create_trans_code():
    return ''.join(random.choices(string.digits, k=6))
'''
def create_funding_code():
	return ''.join(random.choices(string.digits, k=9))
'''


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



# Create Ads fuction 
def Ads(request):
	form = AdsForm(request.POST, request.FILES or None)
	if request.method == 'POST':
		if form.is_valid():
			title = form.cleaned_data.get('title')
			text = form.cleaned_data.get('message')
			img = form.cleaned_data.get('image')
			display = form.cleaned_data.get('display')
			start_date = form.cleaned_data.get('start_date')
			end_date= form.cleaned_data.get('end_date')
			
			ads = Advert(
				title = title,
			    message = text,
			    image = img,
			    slug= title,
			    start_date = start_date,
			    end_date = end_date,
			    display_section = display
				)
			ads.save()
			messages.info(request, "your ads has been submited for a review")
			return redirect('/ads')
	

	context= {
	'form':form
	}
	return render(request, 'dashboard/ads-pay.html', context)





# client detail page 
def my_account(request, code):
	client = UserProfile.objects.get(client_code=code)
	userAcc = UserAccount.objects.get(user=client.user)
	trans= Transactions.objects.filter(account=userAcc)
	orders = client.order_set.all()
	total_order = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()
	out_delivery = orders.filter(status='Out for Delivery').count()
	form = ImageUploadForm()
	if request.method =='POST':
		form = ImageUploadForm(request.POST, request.FILES)
		if form.is_valid():	
			photo = form.cleaned_data.get('img')
			client.image = photo
			client.save()
			messages.success(request, 'profile photo has been updated')

	context= {
	'form':form,
	'client': client, 'orders': orders, 
	'total_order': total_order, 'delivered': delivered, 'pending': pending, 
	'out_delivery':out_delivery, 'trans':trans}
	return render(request, 'dashboard/page-user.html', context)


def edit_account(request, code):
	client = UserProfile.objects.get(client_code=code)
	form = AccountForm(instance=client)
	if request.method == 'POST':
		form = AccountForm(request.POST , instance=client) 
		if form.is_valid():
			messages.success(request, 'Great profile has been updated ')
			form.save()

	context ={
	'form':form,
	'client':client,
	
	}
	return render (request, 'dashboard/edit-account.html', context)


# wallet page and function 
def wallet(request, code):
	client = UserProfile.objects.get(client_code=code)
	bank = UserAccount.objects.get(user=client.user)
	trans= Transactions.objects.filter(account=bank)
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
	'trans':trans,
	'form':form,
	'tform':TopUpForm(),
	'wform': TransForm(),
	'sform': SavForm(),
	'sendform':SendMoneyForm(),
	'accnform':ConfirmAccountForm(),
	'payStack':PaystackForm(),
	'pk_key':settings.PAYSTACK_PUBLIC_KEY
	}
	return render (request, 'dashboard/wallet.html', context)



# top up funds function 
# Top up funds confirmation funtion 
def topup_confirm(request):
	if request.method == "POST":
		tr_code = request.POST.get('code')
		staff = request.POST.get('user_id')
		trans = Transactions.objects.get(ref_code=tr_code)
		wallet = UserAccount.objects.get(user=trans.account.user)
		staff_profile = UserProfile.objects.get(user=staff)

		# Identifiying and keeping record of who count and approved a transaction 
		approver = TopupConfirm(
			amount=trans.amount,
			trans_ref=tr_code,
			)
		approver.approved_by = staff_profile 
		new_wal =  wallet.wallet_balance + trans.amount

		# updating the other 

		trans.status = 'Credited'
		wallet.wallet_balance = new_wal

		approver.save()
		wallet.save()

		trans.save()	

		'''
		TODO: HANDLING THE RESPONSE 


		'''

		tr = Transactions.objects.all()
		trans= tr.filter(status='Pending').order_by('-time')
		con = Transaction.objects.values().filter(status='Pending').order_by('-time')

		trans_data = list(con)
	

		return JsonResponse({'status':200, 'message':'Topup confirm', 'new_wallet':new_wal, 'trans_data':trans_data})
	else:
	
		return JsonResponse({'status':300, 'message':'Order does not exists'})

	return JsonResponse({'status':00, })
	

# top up funds request function 
def topUp(request):
	if request.method == "POST":
		acctUserid = request.POST.get('actUser')
		payment = request.POST.get('pay')
		amount = request.POST.get('amount')
		userAcc = UserAccount.objects.get(id=acctUserid)
		client = UserProfile.objects.get(id=acctUserid)
		email = client.email
		bal = userAcc.wallet_balance
		trans_ref = create_trans_code()		
		if payment == 'C':
			t_note = "Cash topup request, waiting to confirm cash"
			top_wallet = Transactions(
					transaction_type= 'Topup',
					payment_type = 'Cash',
					date= date ,
					time= time,
					note = t_note,
					amount = amount,
					ref_code = trans_ref,
					)
			top_wallet.account = userAcc

			top_wallet.save()
			return JsonResponse({'status':'Save', 'pending_fund':amount, 'pay_type':payment, 'trans_code':trans_ref, 'wallet':bal})

			print("successfully funded account. new balance will reflect in approximately 20min.")

		if payment == 'CD':	
			charge = int(amount) / 100 * 1.5 + 100
			new_amount = int(amount) + charge
			t_note = "Online wallet topUp"
			top_wallet = Transactions(
						transaction_type= 'Topup',
						payment_type = 'Online',
						date= date ,
						time= time,
						note = t_note,
						amount = amount,
						ref_code = trans_ref,
						)
			top_wallet.account = userAcc

			top_wallet.save()	
			return JsonResponse({'status':0, 
				'pending_fund':new_amount, 
				'charge':charge,
				'pay_type':payment,
				'email':email,
				'lname':client.last_name,
				'fname':client.first_name,
				'ref':trans_ref
				})
		# Topup from Flex Account 
		if payment == 'F':	
			if (userAcc.flex_balance >= float(amount)):
				new_wal_bal = userAcc.wallet_balance + float(amount)
				new_flex_bal= userAcc.flex_balance -  float(amount)
				userAcc.wallet_balance = new_wal_bal
				userAcc.flex_balance = new_flex_bal
				userAcc.save()
				t_note = "topup from flex balance"
				top_wallet = Transactions(
							transaction_type= 'Topup',
							payment_type = 'Wallet',
							status='Credited',
							date= date ,
							time= time,
							note = t_note,
							amount = amount,
							ref_code = trans_ref,
							)
				top_wallet.account = userAcc
				top_wallet.save()	
				messages.success(request, "Wallet Balance has been Credited")		
				return JsonResponse({'status':200})
			else:
				messages.warning(request, "Whoops! insufficent funds in your flex balance. Select another option to fund account")
				return JsonResponse({'status':201})
		if payment == 'U':
			t_note = "Ussd code topup request, waiting to confirm alert "
			top_wallet = Transactions(
					transaction_type= 'Topup',
					payment_type = 'Ussd',
					date= date ,
					time= time,
					note = t_note,
					amount = amount,
					ref_code = trans_ref,
					)
			top_wallet.account = userAcc

			top_wallet.save()
			

			print("Pay into the below account to complect topUp")
			return JsonResponse({'status':1, 'pending_fund':amount, 'pay_type':payment, 'trans_code':trans_ref})
		

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
			trans_ref = create_trans_code()

			if (userBal > cash):
				new_balance = userBal - cash
				userAcc.wallet_balance = new_balance
				userAcc.save()
				trans = Transactions(
					transaction_type= 'Withdrawal',
					date= date ,
					time= time,
					amount = cash,
					note = note, 
					ref_code = trans_ref
					)
				trans.account = userAcc
				trans.save()
				return JsonResponse({'status':'Save', 'wallet_balance':new_balance, 'trans_code':trans_ref})

			elif (userBal < cash ):
				return JsonResponse({'status':1, 'wallet_balance':userBal})

			elif (userBal <= cash ):
				return JsonResponse({'status':2, 'wallet_balance':userBal})

			else:
				return JsonResponse({'status':0, })

# sending money account function 
# Confirm send moeny to mek account function 
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
				return JsonResponse({'status':200,
				 'response':response,
				 'bank':bnk, 'number':account_number, 
				 'acc_type': account_type})
					
			except Exception as e:
				return JsonResponse({'status':100 })
			
		if account_type == 'Other':
			return JsonResponse({'status':50,
				'number':account_number, 
				 'acc_type': account_type,
				})

	return JsonResponse( { 'status': 0})


# send money to other account function 
def send_money(request):
	if request.method == "POST":
		account_type = request.POST.get('account_type')
		sender = request.POST.get('sender')
		amount = request.POST.get('amount')
		rec_account_name = request.POST.get('account')
		bank = request.POST.get('bank')
		account_number = request.POST.get('account_num')
		senderAcc = UserAccount.objects.get(id=sender)	
		senderBal = senderAcc.wallet_balance
		cash = float(amount)
		low_cash = float(300)


		# checking if its mek account to get the account number 
		if account_type == 'Mek':
			rec_account = UserProfile.objects.get(client_code=account_number)
			rec_data = UserAccount.objects.get(user=rec_account.user)
			#print(rec_account)
			#print(rec_data)
			send_note = "Transfered to " + str(rec_data)  
			rec_note = "Recieved Funds from  " + str(senderAcc)

			recBal = rec_data.wallet_balance

			# Checking Senders Account and deductin the amount 
		
			if (senderBal <= low_cash ):
				return JsonResponse({'status':300, 'wallet_balance':senderBal})

			elif (senderBal > cash ):
				new_balance = senderBal - cash
				senderAcc.wallet_balance = new_balance
				senderAcc.save()
				trans_code = create_trans_code()

				# Creating sender's transaction 
				sender_trans = Transactions(
					transaction_type= 'Send',
					date= date ,
					time= time,
					note = send_note,
					amount = cash,
					status= 'Debited',
					ref_code = trans_code 
					)
				sender_trans.account = senderAcc
				sender_trans.save()

				# Creating recievers's transaction 
				rec_new_bal = recBal + cash 
				rec_data.wallet_balance = rec_new_bal
				rec_data.save()

				reciever_trans = Transactions(
					transaction_type= 'Topup',
					date= date ,
					time= time,
					note= rec_note,
					amount = cash,
					status= 'Credited',
					ref_code = trans_code ,
					)
				reciever_trans.account = rec_data
				reciever_trans.save()

				return JsonResponse({'status':200, 'wallet_balance':new_balance, 'reciever_wallet_balance':rec_new_bal, 'trans_code':trans_code })

			elif (senderBal < cash ):
				return JsonResponse({'status':100, 'wallet_balance':senderBal})

			elif (senderBal <= cash ):
				return JsonResponse({'status':350, 'wallet_balance':senderBal})

			else:
				return JsonResponse({'status':0, })


		# Functions for sendind cash to other bank 
		if account_type == 'Other':
			#print(rec_account)
			#print(rec_data)
			send_note = "Sendind to " + bank  + " bank " + " Num: " +  account_number  +  " Name: " + rec_account_name  
			# Checking Senders Account and deductin the amount 
			if (senderBal <= low_cash ):
				return JsonResponse({'status':300, 'wallet_balance':senderBal})

			elif (senderBal > cash ):
				new_balance = senderBal - cash
				senderAcc.wallet_balance = new_balance
				senderAcc.save()

				ref_code = create_trans_code(),

				# Creating sender's transaction 
				sender_trans = Transactions(
					transaction_type= 'SE',
					date= date ,
					time= time,
					note = send_note,
					amount = cash,
					status= 'Pending',
					ref_code = ref_code 
					)
				sender_trans.account = senderAcc
				sender_trans.save()

				# Create send hitory model data 

				send_trans = SendHistory(
					account_type= 'Other',
					amount = cash,
    				account_name = rec_account_name,
    				account_number = account_number,
    				bank_name = bank,
   					trans_ref = ref_code, 
					)
				send_trans.sender = senderAcc
				send_trans.save()

				return JsonResponse({'status':200, 'wallet_balance':new_balance, 'trans_code':ref_code})

			elif (senderBal < cash ):
				return JsonResponse({'status':100, 'wallet_balance':senderBal})

			elif (senderBal <= cash ):
				return JsonResponse({'status':350, 'wallet_balance':senderBal})

			else:
				return JsonResponse({'status':0, })


	return JsonResponse( { 'status':'ok'})



#Invest money from wallet function 
def invest(request):
	if request.method == "POST":
		acctUserid = request.POST.get('actUser')
		duration = request.POST.get('pay_day')
		amount = request.POST.get('amount')
		userAcc = UserAccount.objects.get(id=acctUserid)
		userBal = userAcc.wallet_balance
		user_save_Bal = userAcc.sav_balance
			# converting the form field amount to float 
		cash = float(amount)

		trans_code = create_trans_code()

		if (userBal > cash and  float(duration) > 2):
			new_balance = userBal - cash
			new_sav_balance = user_save_Bal + cash
			userAcc.wallet_balance = new_balance
			userAcc.sav_balance = new_sav_balance
			userAcc.save()

			# Calculating Future pay_day
			pay_d = d + relativedelta(months=+int(duration))

			sav_note = " savings duration is " + str(pay_d)

			
  			#pay_d = date + timedelta(days=24)
			trans = Transactions(
				transaction_type= 'Save',
				status= 'Debited',
				date= date ,
				note=sav_note,
				time= time,
				amount = cash,
				ref_code = trans_code,
				)
			trans.account = userAcc
			trans.save()
			
			save_funds = Saving(
				amount = cash,
				save_date = date,
				pay_date = pay_d,
				ref_code = trans_code,

				)
			save_funds.owner = userAcc

			save_funds.save()
			
			return JsonResponse({'status':'Save', 'wallet_balance':new_balance, 'sav_balance':new_sav_balance, 'pay_out':pay_d})

		elif (userBal > cash and  float(duration) < 3 ):
			return JsonResponse({'status':100, 'wallet_balance':userBal})
		

		elif (userBal < cash ):
			return JsonResponse({'status':1, 'wallet_balance':userBal})

		elif (userBal <= cash ):
			return JsonResponse({'status':2, 'wallet_balance':userBal})

	else:
		return JsonResponse({'status':0, })

@login_required
def trans_history(request, code):
	client = UserProfile.objects.get(client_code=code)
	bank = UserAccount.objects.get(user=client.user)
	trans = bank.transactions_set.all().order_by('-date')
	topup = bank.transactions_set.filter(status='Pending', transaction_type='T').order_by('-date')
	context={
	'topup':topup,
	'client':client,
	'bank':bank,
	'trans':trans,
	}
	return render(request, 'dashboard/trans-history.html', context)
	#return render(request, 'dashboard/ui-notifications.html', context)



class VendorView(ListView):
	template_name = "dashboard/vendor-dashboard.html"
	model = Seller
	#model = Vpayment


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
			password = form.cleaned_data.get('password1')
			email = form.cleaned_data.get('email')
			group = Group.objects.get(name='client')
			user.groups.add(group)

			#client_code = create_unique_code()
			messages.success(request, 'Account was created for ' + username )
			
			#return redirect('login')

			#authenticating the fields through django authentication package 
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('my-account/'+client_code)

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


#Update UserProfile to trader account 

@login_required
@trader_only
def TraderAccount(request):
	form = SellerForm()
	if request.method == 'POST':
		form = SellerForm(request.POST, request.FILES)
		if form.is_valid():
			owner = form.cleaned_data.get('seller_number')
			bus_name = form.cleaned_data.get('business_name')
			goods = form.cleaned_data.get('goods')
			services = form.cleaned_data.get('services')
			fastFood = form.cleaned_data.get('fast_food')
			skill = form.cleaned_data.get('skill')
			descrip = form.cleaned_data.get('description')
			address = form.cleaned_data.get('address')
			city = form.cleaned_data.get('city')
			img = form.cleaned_data.get('image')
			tel_1 = form.cleaned_data.get('tel_one')
			tel_2 = form.cleaned_data.get('tel_two')
			try:
				seller = UserProfile.objects.get(client_code=owner)
				if seller.is_seller == True:
					messages.info(request, 'this user already has a trading account')
					return redirect('/trader-account')
				else:
					trader = Seller(
						owner = seller,
						business_name=bus_name,
						description=descrip,
						address=address,
						fast_food=fastFood,
						goods=goods,
						services=services,
						skill=skill,
						image=img,
						tel_one=tel_1,
						tel_two=tel_2
						)
					trader.save()
					seller.is_seller = True
					seller.save()
					messages.success( request, 'User have been upgradered to a trader account')
					return redirect('/trader-account')
			except Exception as e:
				messages.info(request, 'user does not exist, check your user number and try again ')
				return redirect('/trader-account')
			else:
				pass
		
	context = {
	'form':form
	}
	return render(request, 'dashboard/seller.html', context)
	

# Edit Busines Details function 
def Edit_business(request, code):
	client = UserProfile.objects.get(client_code=code)
	sel = Seller.objects.get(owner=client)
	form = SellerUpdatForm(instance=sel)
	if request.method == 'POST':
		form = SellerUpdatForm(request.POST , instance=sel) 
		if form.is_valid():
			form.save()
			messages.success(request, 'store has been updated')
			return redirect('/trader-account')

	context = {
	'form':form,
	'sel':sel
	}

	return render(request, 'dashboard/edit-seller.html', context)



#User Dasbard View 
@login_required(login_url ='login')
#@admin_only
def order_history(request):
	orders = request.user.order_set.filter().order_by('-ordered_date')
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
	return render(request, 'dashboard/order_history.html', context)


def password(request):
	return render(request, 'user_account/password.html',{"title":password})

# This is for the Sales Admin Dashboard 
# AdminDashbod View 
@login_required(login_url ='login')
@admin_only
#@allowed_users('admin')
def admin_dashboard(request):
	#clients = UserProfile.objects.all()
	orders = Order.objects.all().order_by('-ordered_date')
	total_order = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()
	out_delivery = orders.filter(status='Out for Delivery').count()
	context = {
	#'clients':clients,
	'orders':orders,
	'total_order':total_order,
	'delivered':delivered,
	'pending':pending,
	'out_delivery':out_delivery,

	}
	return render(request, 'dashboard/sales-dashboard.html', context)

	#return render(request, 'admin_account/dashboard.html', context)



# cleark or CFO dashboard 
def admin_cleark(request):
	form = ConTopUpForm()
	tr = Transactions.objects.all()
	trans= tr.filter(status='Pending').order_by('-time')
	client = request.user.userprofile.client_code
	order = Order.objects.all()
	orders = order.filter(status='Delivered')
	delivered = order.filter(status='Delivered').count()
	context = {
	'trans':trans,
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
