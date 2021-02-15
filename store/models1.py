from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Sum
from django.shortcuts import reverse 
from django_countries.fields import CountryField
from staffs.models import * 
# Create your models here.

class Customer(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True )
	email = models.CharField(max_length=200, null=True )
	phone = models.CharField(max_length=200, null=True )
	date_created = models.DateTimeField(auto_now_add= True, null=True )

	def __str__(self):
		return self.name

# This counld be option- its said to be the link btwn product and order 
class Tag(models.Model):
	name = models.CharField(max_length=200, null=True )

	def __str__(self):
		return self.name 

# main store product model 
class MallProduct(models.Model):
	CATHEGORY= (
		('Food', 'Food'),
		('Food Item', 'Food Item')

		)
	LABEL_CHOICES= (
		('P', 'primary'),
		('S', 'secondary'),
		('D', 'danger'),
		)
	name = models.CharField(max_length=200, null=True )
	price = models.FloatField( null=True )
	discount_price = models.FloatField( blank=True, null=True )
	cathegory = models.CharField(max_length=200, null=True, choices=CATHEGORY)
	description = models.CharField(max_length=200, null=True )
	date_created = models.DateTimeField(auto_now_add= True, null=True )
	tag = models.ManyToManyField(Tag)
	lable = models.CharField(choices=LABEL_CHOICES, max_length=2, null=True,)
	slug = models.SlugField()

	def __str__(self):
		return self.name 


	def get_absolute_url(self):
		return reverse("product", kwargs={
			'slug':self.slug
			}
			)
	def get_add_to_cart_url(self):
		return reverse("add-to-cart", kwargs={
			'slug':self.slug
			}
			)

	def get_remove_from_cart_url(self):
		return reverse("remove-form-cart", kwargs={
			'slug':self.slug
			}
			)

# product or service order model 
class Product(models.Model):
	CATHEGORY= (
		('G', 'Goods'),
		('S', 'Services')

		)
	name = models.CharField(max_length=200, null=True )
	price = models.FloatField( null=True )
	cathegory = models.CharField(max_length=200, null=True, choices=CATHEGORY)
	description = models.CharField(max_length=200, null=True )
	date_created = models.DateTimeField(auto_now_add= True, null=True )
	slug = models.SlugField()


	def __str__(self):
		return self.name 

class OrderItem(models.Model):
	customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
	item = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)
	is_ordered= models.BooleanField(default=False, null=True, blank=False)

	def __str__(self):
		return f"{self.quantity} of {self.item.name}"

	def get_total_item_price(self):
		return self.quantity * self.item.price

	def get_total_discount_item_price(self):
		return self.quantity * self.item.discount_price

	def get_amount_save(self):
		return self.get_total_item_price() - self.get_total_discount_item_price()

	def get_final_price(self):
		if self.item.discount_price:
			return self.get_total_discount_item_price()
		return self.get_total_item_price()

	def get_total_cart(self):
		total = 0
		for item in get_final_price():
		    total += item.get_final_price()
		total -= self.coupon.amount
		return total


class Address(models.Model):
	customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
	client_name = models.CharField(max_length=200 )
	street_address = models.CharField(max_length=200 )
	apartment_address = models.CharField(max_length=200 )
	
	#payment_option = models.CharField(max_length=200 )
	def __str__(self):
		return self.street_address

	class Meta:
	    verbose_name_plural = 'Addresses'

class Payment(models.Model):
	stripe_charge_id = models.CharField(max_length=50)
	customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL, blank=True)
	amount = models.FloatField()
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.customer.name

class Coupon(models.Model):
	code = models.CharField(max_length=15)
	amount = models.FloatField()

	def __str__(self):
		return self.code 


"""
#TODO: add delivery charges to the item. yet to deciede on the amount 
base on KG per item or KM/distance 
"""
class Delivery(models.Model):
	agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True )
	amount = models.FloatField()

	def __str__(self):
		return self.agent 



class Order(models.Model):
	STATUS= (
		('Pending', 'Pending'),
		('Out for Delivery', 'Out for delivery'),
		('Delivered', 'Delivered'),
		)
	customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
	client_id = models.CharField(max_length=200, null=True, blank=True)
	#client = models.ForeignKey(Client, null=True, on_delete=models.SET_NULL)
	ref_code = models.CharField(max_length=20)
	item = models.ManyToManyField(OrderItem)
	date_created = models.DateTimeField(auto_now_add=True, null=True )
	status = models.CharField(max_length=200, null=True, choices=STATUS, default='Pending')
	is_ordered= models.BooleanField(default=False, null=True, blank=False)
	order_note = models.CharField(max_length=200, null=True, blank=True)
	#shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
	amount = models.FloatField(null=True, blank=True)
	coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, null=True, blank=True)
	refund_requested=models.BooleanField(default=False)
	refund_granted= models.BooleanField(default=False)
	delivery_cost = models.ForeignKey(Delivery, on_delete=models.SET_NULL, null=True, blank=True )
	vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True )
	agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True )
	payment_option = models.CharField(max_length=50, null=True, blank=True)
	#amount = models.ForeignKey( Payment, on_delete=models.SET_NULL, null=True, blank=True)
	

	"""docstring for Order"""
	def __str__(self):
		return self.customer.name


 def get_total(self):
        total = 0
        for order_item in self.product.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total





	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total

		get_final_price

	# total quantity of itmes in cart 
	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total



# not working 

	



class Confirmed(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE)
	client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
	accepted = models.BooleanField(default=False)


	def __str__(self):
		return f"{self.pk}"


class Refund(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE)
	reason = models.TextField()
	accepted = models.BooleanField(default=False)
	email = models.EmailField()

	def __str__(self):
		return f"{self.pk}"







"""

	customer 
	client_name 
	street_address 
	apartment_address  
	country 
	zip_code 
	same_shipping_address 
	save_info 
	payment_option 
"""
	
