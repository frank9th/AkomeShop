import random
import string
import stripe
from decouple import config 
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic import ListView, DetailView, View
import requests 
from .forms import *
from .models import *
from django.db.models import Q
from staffs.models import *
import datetime
from staffs.views import *

t = datetime.datetime.now()
d = datetime.datetime.now()

#datetime.today().strftime('%Y-%m-%d')

time = t.strftime("%X")
date = d.strftime('%Y-%m-%d')


stripe.api_key = settings.STRIPE_SECRET_KEY  




def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


# Home fuction 
class HomeView(ListView):
    model = Product
    #paginate_by = 10
    #template_name = "home.html"
    template_name = "index.html"
    #template_name = "welcome.html"




# Product listing function 
@login_required
def products(request):
    context = {
        'items': Product.objects.all()
    }
    return render(request, "products.html", context)

# Product category function 
def product_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.all()
    context= {'category':category, 'products':products}
    return render(request, "category_page.html", context)

# Product Listing 
@login_required
def ProductList(request):
    products = Product.objects.all()
    context ={
    'products':products
    }
    return render(request, 'dashboard/product_list.html', context)






# Add product function 
def AddProduct(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            sel = form.cleaned_data.get('seller')
            img = form.cleaned_data.get('image')
            img2 = form.cleaned_data.get('image_two')
            img3 = form.cleaned_data.get('image_three')
            cost_price = form.cleaned_data.get('cost_price')
            price = form.cleaned_data.get('price')
            disc_price = form.cleaned_data.get('discount_price')
            short_desc = form.cleaned_data.get('short_desc')
            description = form.cleaned_data.get('description')
            tag = form.cleaned_data.get('tag')
            cate = form.cleaned_data.get('category')
            label = form.cleaned_data.get('label')
            unit = form.cleaned_data.get('unit')
            active = form.cleaned_data.get('active')

            print(unit)

            try:
                seller = UserProfile.objects.get(client_code=sel)
                if seller.is_seller == True:
                    seller_acct = UserAccount.objects.get(user=seller.user)

                    category = Category.objects.get(name=cate)
                    
                    product = Product(
                        category = category,
                        seller = seller_acct,
                        title = title,
                        cost_price = cost_price,
                        price = price,
                        discount_price = disc_price,
                        tag = tag,
                        label = label,
                        slug = title + create_slug(),
                        short_desc = short_desc,
                        description = description,
                        image = img,
                        image_two = img2,
                        image_three = img3,
                        unit=unit,
                        active=active
                        )

                    product.save()
                    messages.success(request, "Product has been added")

                    return redirect('/product')
                else:
                    seller.is_seller == False
                    messages.warning(request, "Whoops this user those not have a business account \n Upgrade user account and try again. ")
                    return redirect('/product')

            except ObjectDoesNotExist:
                messages.warning(request, "Something went wrong")  
                #form.save()
                return redirect('/product')
    else:
        form = ProductForm()
        context = {
        'form':form,
        }
        return render(request, "dashboard/add_product.html", context)

'''
def AddStoreProduct(request, pk):
    user_code = UserProfile.objects.get(id=pk)
    admin= Seller.objects.get(owner=user_code)
    owner = UserAccount.objects.get(user=user_code.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            sel = form.cleaned_data.get('seller')
            img = form.cleaned_data.get('image')
            img2 = form.cleaned_data.get('image_two')
            img3 = form.cleaned_data.get('image_three')
            cost_price = form.cleaned_data.get('cost_price')
            price = form.cleaned_data.get('price')
            disc_price = form.cleaned_data.get('discount_price')
            short_desc = form.cleaned_data.get('short_desc')
            description = form.cleaned_data.get('description')
            tag = form.cleaned_data.get('tag')
            cate = form.cleaned_data.get('category')
            label = form.cleaned_data.get('label')
            unit = form.cleaned_data.get('unit')
            active = form.cleaned_data.get('active')

            print(unit)

            try:
                seller = UserProfile.objects.get(client_code=sel)
                if seller.is_seller == True:
                    seller_acct = UserAccount.objects.get(user=seller.user)

                    category = Category.objects.get(name=cate)
                    
                    product = Product(
                        category = category,
                        seller = seller_acct,
                        title = title,
                        cost_price = cost_price,
                        price = price,
                        discount_price = disc_price,
                        tag = tag,
                        label = label,
                        slug = title + create_slug(),
                        short_desc = short_desc,
                        description = description,
                        image = img,
                        image_two = img2,
                        image_three = img3,
                        unit=unit,
                        active=active
                        )

                    product.save()
                    messages.success(request, "Product has been added")

                    return redirect('/product')
                else:
                    seller.is_seller == False
                    messages.warning(request, "Whoops this user those not have a business account \n Upgrade user account and try again. ")
                    return redirect('/product')

            except ObjectDoesNotExist:
                messages.warning(request, "Something went wrong")  
                #form.save()
                return redirect('/product')
    else:
        form = ProductForm()
        context = {
        'form':form,
        'owner':owner,
        }
        return render(request, "dashboard/add_product.html", context)

'''

# Get Requst to product update page 
def UpdateProduct(request, pk):
    product = Product.objects.get(id=pk)
    form = UpdateProductForm(instance=product)
    context = {
    'product': product,
    'form':form,
    }
    return render(request, 'dashboard/update_product.html', context)



# POST Requst to product update page 
def UpdateStore(request):
    if request.method == 'POST':
        pk = request.POST.get('id')
        product = Product.objects.get(id=pk)
        title = request.POST.get('title')
        cost = request.POST.get('cost')
        discount = request.POST.get('discount')
        amount = request.POST.get('amount')
        short = request.POST.get('short')
        desc = request.POST.get('desc')
        img = request.POST.get('img')
        status = request.POST.get('status')
        cat = request.POST.get('cathegory')
        tag = request.POST.get('tag')
        lable = request.POST.get('lable')
        unit = request.POST.get('unit')
        active = request.POST.get('active')
        img2 = request.POST.get('img2')
        img3 = request.POST.get('img3')

        if unit == None:
            unit = False
        else:
            unit = True

        if active == 'on':
            active = True
        else:
            active = False

        # Get category from categories
        category = Category.objects.get(id=cat)

        # Updating the product   
        product.category = category
        product.title = title
        product.price = amount 
        if cost != '':
            product.cost_price = cost
        
        if discount != '':
            product.discount_price = discount
        product.short_desc = short
        product.description = desc
        product.tag = tag
        product.label = lable
        product.unit = unit
        product.status = status
        product.active = active
        #product.image = img
        #product.image_two = img2
        #product.image_three = img3

        product.save() 
        return JsonResponse({'status':200, 'message':'Item has been updated!',})
        
  
    messages.warning(request, "Whoops! something went wrong. try again")
    return JsonResponse({'status':300, 'message':'Whoops! something went wrong. try again'})


# Delete store product  
def delete_store_product(request, pk):
    product = Product.objects.get(id=pk) 
    product.delete() # saving the data in the db 
    messages.success(request,  'product has been deleted')
    return redirect('/product-list')

 



# Fastfood listing page 
def FoodSellers(request):
    seller = Seller.objects.filter(fast_food=True)
    context= {
    'seller':seller
    }
    return render(request, 'food_sellers.html', context)


# Fast Food page 
def FastFood(request, code):
    #print(shop)
    #print(shop.owner)
    #print(shop.owner.client_code)
    #user_code = UserProfile.objects.get(user=shop.owner.user)
    user_code = UserProfile.objects.get(client_code=code)
    admin= Seller.objects.get(owner=user_code)
    owner = UserAccount.objects.get(user=user_code.user)
    item = Product.objects.filter(seller=owner, tag='FS')
    print(item)
    print(admin)
    context= {
    'item':item,
    'admin':admin
    }
    return render(request, 'fast_food.html', context)


# Product Listing 
def SellerProduct(request, code):
    user_code = UserProfile.objects.get(client_code=code)
    admin= Seller.objects.get(owner=user_code)
    owner = UserAccount.objects.get(user=user_code.user)
    products = Product.objects.filter(seller=owner)  
    context ={
    'products':products,
    'owner':owner,
    }
    return render(request, 'dashboard/product_list.html', context)








def ServicePage(request):
    serve = Product.objects.filter(tag= 'S' )
    context = {
    'serve':serve
    }
    return render(request, 'service_page.html', context)






# Search product function 
def search(request):
    query = request.GET.get('query')
    products = Product.objects.filter(Q(title__icontains=query) |  Q(description__icontains=query))
    context = {
    'query':query,
    'products':products
    }
    return render(request, 'search.html', context)


# Form validation function 
def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid


# Cart function 
def cart(request):
    #form= CreataOrderForm()
    couponForm = CouponForm()
    form = OrderForm()
    customer = request.user
    if request.method =='POST':
        #print('Printing post:', request.POST)
        form = OrderForm(request.POST, instanc) # throwing the post data into the form 
        if form.is_valid(): # performing valid check 

            form.save() # saving the data in the db 
            return redirect('checkout')

    context= {'form':form, 'couponForm':couponForm}
    return render(request, 'store/checkout.html', context)

# checkout with clients code 
def clientCheckout(request):
    form = ClientCheckOutForm(request.POST or None)  
    order = {} 
    #form = OrderModelForm(request.POST or None)
    try:
        order = Order.objects.get(user=request.user, ordered=False)
        if form.is_valid():
            # Geting the specified fields 
            order_note = form.cleaned_data.get('additional_note')   
            payment_option = form.cleaned_data.get('payment_option')

            # TODO: Add redirect to the selected payment option 
            #return redirect('home')
            if payment_option == 'S':
                return redirect('store:payment', payment_option='stripe')

            elif payment_option == 'P':
                return redirect('store:payment', payment_option='paypal')
            # Pay with wallet function 
            if payment_option == 'W':
                client = order.client
                client_wal = UserAccount.objects.get(user=client.user)
                clientBal = client_wal.wallet_balance
                total = order.ground_total()
                if (clientBal > total):
                    new_balance = clientBal - total
                    client_wal.wallet_balance = new_balance
                    client_wal.save()
                    order_ref_code = create_ref_code()
                     # create the payment
                    payment = Payment()
                    payment.user = request.user
                    #payment.amount = order.get_total()
                    payment.amount = order.ground_total()
                    payment.ref_code = order_ref_code
                    payment.save()
                    # assign the payment to the order
                    order_items = order.items.all()
                    order_items.update(ordered=True)
                    for item in order_items:
                        if item.item.cost_price:
                            sel_amount = item.quantity * item.item.cost_price
                        #geting the seller of the item 
                            seller = item.item.seller

                        # adding each item price to the seller's flex balance 
                            new_flex_bal = seller.flex_balance + sel_amount

                            seller.flex_balance = new_flex_bal

                            seller.save()
                            print(item.item.seller.wallet_balance)
                            item.save()
                        else:
                            sel_amount = item.quantity * item.item.price
                            seller = item.item.seller

                        # adding each item price to the seller's flex balance 
                            new_flex_bal = seller.flex_balance + sel_amount

                            seller.flex_balance = new_flex_bal

                            seller.save()
                            #print(item.item.seller.wallet_balance)
                            item.save()
                    order.ordered = True
                    order.payment = payment
                    #order.client = client_infor
                    order.ordered_date = date
                    order.ordered_time = time
                    order.note = order_note
                    order.ref_code = order_ref_code
                    order.save()

                    t_note = "Your Acct " + client.client_code + " Has Been Debited "
                    trans = Transaction(
                            transaction_type= 'Debit',
                            status= 'Debited',
                            date= date ,
                            time= time,
                            note = t_note,
                            amount = order.ground_total(),
                            ref_code = order_ref_code,
                            )
                    trans.account = client_wal
                    trans.save()
                    messages.success(request, "Your order was successful!")
                    return redirect("/")

                elif (clientBal < total ):
                    messages.info(request, "Whoops! infuficent funds")
                    #return JsonResponse({'status':1, 'wallet_balance':userBal})
                    return redirect("/confirm-checkout")

                elif (clientBal <= total ):
                    messages.info(request, "infuficent funds. topup your account or select a different payment option")
                    #return JsonResponse({'status':1, 'wallet_balance':userBal})
                    return redirect("/confirm-checkout")

                else:
                    return JsonResponse({'status':0, })

            elif payment_option == 'PD':
                    order_ref_code = create_ref_code()
                     # create the payment
                    payment = Payment()
                    payment.user = request.user
                    #payment.amount = order.get_total()
                    payment.amount = order.ground_total()
                    payment.ref_code = order_ref_code
                    payment.save()
                    # assign the payment to the order
                    order_items = order.items.all()
                    order_items.update(ordered=True)
                    for item in order_items:
                        if item.item.cost_price:
                            sel_amount = item.quantity * item.item.cost_price
                        #geting the seller of the item 
                            seller = item.item.seller

                        # adding each item price to the seller's flex balance 
                            new_flex_bal = seller.flex_balance + sel_amount

                            seller.flex_balance = new_flex_bal

                            seller.save()
                            print(item.item.seller.wallet_balance)
                            item.save()
                        else:
                            sel_amount = item.quantity * item.item.price
                            seller = item.item.seller

                        # adding each item price to the seller's flex balance 
                            new_flex_bal = seller.flex_balance + sel_amount

                            seller.flex_balance = new_flex_bal

                            seller.save()
                            #print(item.item.seller.wallet_balance)
                            item.save()
                    order.ordered = True
                    order.payment = payment
                    #order.client = client_infor
                    order.ordered_date = date
                    order.ordered_time = time
                    order.note = order_note

                    order.ref_code = order_ref_code
                    order.save()
                    messages.success(request, "Your order was successful!")
                    return redirect("/")
            else:
                messages.warning(
                    self.request, "Invalid payment option selected")
                return redirect('store:checkout')

    except ObjectDoesNotExist:
        messages.error(request, "You do not have an active order")
    #return render(request, 'home')

    context= {'form':form, 
    #'item':item, 
    'couponform':CouponForm(), 
    'order':order, 
    'client_code':ClientCodeForm(),
    #'client_dstails':client_dstails
    }
    #messages.warning(request, "Failed checkout")
    return render(request, 'checkout-page.html', context)

# checkout to enter client details
class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'couponform': CouponForm(),
                'client_code':ClientCodeForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': True
            }

            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='S',
                default=True
            )
            if shipping_address_qs.exists():
                context.update(
                    {'default_shipping_address': shipping_address_qs[0]})

            billing_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='B',
                default=True
            )
            if billing_address_qs.exists():
                context.update(
                    {'default_billing_address': billing_address_qs[0]})
            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("store:checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():

                use_default_shipping = form.cleaned_data.get(
                    'use_default_shipping')
                if use_default_shipping:
                    print("Using the defualt shipping address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='S',
                        default=True
                    )
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default shipping address available")
                        return redirect('store:checkout')
                else:
                    print("User is entering a new shipping address")
                    shipping_address1 = form.cleaned_data.get(
                        'shipping_address')
                    shipping_address2 = form.cleaned_data.get(
                        'shipping_address2')
                    shipping_country = form.cleaned_data.get(
                        'shipping_country')
                    shipping_zip = form.cleaned_data.get('shipping_zip')

                    if is_valid_form([shipping_address1, shipping_country, shipping_zip]):
                        shipping_address = Address(
                            user=self.request.user,
                            street_address=shipping_address1,
                            apartment_address=shipping_address2,
                            country=shipping_country,
                            zip=shipping_zip,
                            address_type='S'
                        )
                        shipping_address.save()

                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get(
                            'set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required shipping address fields")

                use_default_billing = form.cleaned_data.get(
                    'use_default_billing')
                same_billing_address = form.cleaned_data.get(
                    'same_billing_address')

                if same_billing_address:
                    billing_address = shipping_address
                    billing_address.pk = None
                    billing_address.save()
                    billing_address.address_type = 'B'
                    billing_address.save()
                    order.billing_address = billing_address
                    order.save()

                elif use_default_billing:
                    print("Using the defualt billing address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='B',
                        default=True
                    )
                    if address_qs.exists():
                        billing_address = address_qs[0]
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default billing address available")
                        return redirect('store:checkout')
                else:
                    print("User is entering a new billing address")
                    billing_address1 = form.cleaned_data.get(
                        'billing_address')
                    billing_address2 = form.cleaned_data.get(
                        'billing_address2')
                    billing_country = form.cleaned_data.get(
                        'billing_country')
                    billing_zip = form.cleaned_data.get('billing_zip')

                    if is_valid_form([billing_address1, billing_country, billing_zip]):
                        billing_address = Address(
                            user=self.request.user,
                            street_address=billing_address1,
                            apartment_address=billing_address2,
                            country=billing_country,
                            zip=billing_zip,
                            address_type='B'
                        )
                        billing_address.save()

                        order.billing_address = billing_address
                        order.save()

                        set_default_billing = form.cleaned_data.get(
                            'set_default_billing')
                        if set_default_billing:
                            billing_address.default = True
                            billing_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required billing address fields")

                payment_option = form.cleaned_data.get('payment_option')

                if payment_option == 'S':
                    return redirect('store:payment', payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('store:payment', payment_option='paypal')
                elif payment_option == 'PD':
                     # create the payment
                    payment = Payment()
                    payment.user = self.request.user
                    #payment.amount = order.get_total()
                    payment.amount = order.ground_total()
                    payment.save()

                    # assign the payment to the order
                    order_items = order.items.all()
                    order_items.update(ordered=True)
                    for item in order_items:
                        item.save()

                    order.ordered = True
                    order.payment = payment
                    order.ref_code = create_ref_code()
                    order.save()

                    messages.success(self.request, "Your order was successful!")
                    return redirect("/")
                else:
                    messages.warning(
                        self.request, "Invalid payment option selected")
                    return redirect('store:checkout')

                  

        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("store:order-summary")

class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.billing_address:
            context = {
                'order': order,
                'DISPLAY_COUPON_FORM': False,
                'STRIPE_PUBLIC_KEY' : settings.STRIPE_PUBLIC_KEY
            }
            userprofile = self.request.user.userprofile
            if userprofile.one_click_purchasing:
                # fetch the users card list
                cards = stripe.Customer.list_sources(
                    userprofile.stripe_customer_id,
                    limit=3,
                    object='card'
                )
                card_list = cards['data']
                if len(card_list) > 0:
                    # update the context with the default card
                    context.update({
                        'card': card_list[0]
                    })
            return render(self.request, "payment.html", context)
        else:
            messages.warning(
                self.request, "You have not added a billing address")
            return redirect("store:checkout")

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        form = PaymentForm(self.request.POST)
        userprofile = UserProfile.objects.get(user=self.request.user)
        if form.is_valid():
            token = form.cleaned_data.get('stripeToken')
            save = form.cleaned_data.get('save')
            use_default = form.cleaned_data.get('use_default')

            if save:
                if userprofile.stripe_customer_id != '' and userprofile.stripe_customer_id is not None:
                    customer = stripe.Customer.retrieve(
                        userprofile.stripe_customer_id)
                    customer.sources.create(source=token)

                else:
                    customer = stripe.Customer.create(
                        email=self.request.user.email,
                    )
                    customer.sources.create(source=token)
                    userprofile.stripe_customer_id = customer['id']
                    userprofile.one_click_purchasing = True
                    userprofile.save()

            #amount = int(order.get_total() * 100)
            amount = int(order.ground_total() * 100)

            try:

                if use_default or save:
                    # charge the customer because we cannot charge the token more than once
                    charge = stripe.Charge.create(
                        amount=amount,  # cents
                        currency="usd",
                        customer=userprofile.stripe_customer_id
                    )
                else:
                    # charge once off on the token
                    charge = stripe.Charge.create(
                        amount=amount,  # cents
                        currency="usd",
                        source=token
                    )

                # create the payment
                payment = Payment()
                payment.stripe_charge_id = charge['id']
                payment.user = self.request.user
                #payment.amount = order.get_total()
                payment.amount = order.ground_total()
                payment.save()

                # assign the payment to the order

                order_items = order.items.all()
                order_items.update(ordered=True)
                for item in order_items:
                    item.save()

                order.ordered = True
                order.payment = payment
                order.ref_code = create_ref_code()

                order.ordered_date = date
                order.ordered_time = time
                order.note = order_note

                order.save()
                messages.success(self.request, "Your order was successful!")

                #TODO: SEND ORDER TOTAL AND ref_code to client phone 
                return redirect("/")

            except stripe.error.CardError as e:
                body = e.json_body
                err = body.get('error', {})
                messages.warning(self.request, f"{err.get('message')}")
                return redirect("/")

            except stripe.error.RateLimitError as e:
                # Too many requests made to the API too quickly
                messages.warning(self.request, "Rate limit error")
                return redirect("/")

            except stripe.error.InvalidRequestError as e:
                # Invalid parameters were supplied to Stripe's API
                print(e)
                messages.warning(self.request, "Invalid parameters")
                return redirect("/")

            except stripe.error.AuthenticationError as e:
                # Authentication with Stripe's API failed
                # (maybe you changed API keys recently)
                messages.warning(self.request, "Not authenticated")
                return redirect("/")

            except stripe.error.APIConnectionError as e:
                # Network communication with Stripe failed
                messages.warning(self.request, "Network error")
                return redirect("/")

            except stripe.error.StripeError as e:
                # Display a very generic error to the user, and maybe send
                # yourself an email
                messages.warning(
                    self.request, "Something went wrong. You were not charged. Please try again.")
                return redirect("/")

            except Exception as e:
                # send an email to ourselves
                messages.warning(
                    self.request, "A serious error occurred. We have been notifed.")
                return redirect("/")

        messages.warning(self.request, "Invalid data received")
        return redirect("/payment/stripe/")



# Order summary 
class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")

# Item Detail View 
class ItemDetailView(DetailView):
    model = Product
    template_name = "product.html"

# Add to Cart function 
@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
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

# Remove from cart 
@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("store:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("store:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("store:product", slug=slug)

# Remove single item function 
@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("store:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("store:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("store:product", slug=slug)

# Delete Item 
def delete_item(request, pk):
    item = Order.objects.get(id=pk)
    if request.method =='POST':
        #print('Printing post:', request.POST)
            item.delete() # saving the data in the db 
            return redirect('/')


    context= {'item':item}
    return render(request, 'delete.html', context)


# Get Coupon 
def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon does not exist")
        return redirect("store:checkout")


# Add Coupon 
class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                #order.save()
                messages.success(self.request, "Successfully added coupon")
                return redirect("store:checkout")
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("store:checkout")

# Request Refund 
class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {
            'form': form
        }
        return render(self.request, "request_refund.html", context)

    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            # edit the order
            try:
                order = Order.objects.get(ref_code=ref_code)
                order.refund_requested = True
                order.save()

                # store the refund
                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()

                messages.info(self.request, "Your request was received.")
                return redirect("store:request-refund")

            except ObjectDoesNotExist:
                messages.info(self.request, "This order does not exist.")
                return redirect("store:request-refund")

# Client Code 
def get_client_code(request, code):
    try:
        client_code = UserProfile.objects.get(client_code=code)
        return client_code
    except ObjectDoesNotExist:
        messages.warning(request, "Sorry, your code is incorrect")
        return redirect("/")
        #return JsonResponse('Enter a valid code', safe=False)


# Add Client Code 
def AddClientCode(request):
    form = ClientCodeForm(request.POST or None)
    if form.is_valid():
        #code = form.cleaned_data.get('code')
        code = request.POST.get('code') 
        try:
            #client = get_client_code(request, code)
            client = UserProfile.objects.get(client_code=code)   
           
            order = Order.objects.get(
                    user=request.user, ordered=False)
            order.client = client 
            order.save()
            messages.success(request, "Successfully added Client details")

            #messages.info(request, "Thank you ")
            return redirect('/confirm-checkout')

        except ObjectDoesNotExist:
            messages.warning(request, "Client's code is incorrect")
            return redirect('/confirm-checkout')

    