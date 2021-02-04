from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Sum
from django.shortcuts import reverse 
from django_countries.fields import CountryField
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


class Product(models.Model):
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



class BillingAddress(models.Model):
	customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
	client_name = models.CharField(max_length=200 )
	street_address = models.CharField(max_length=200 )
	apartment_address = models.CharField(max_length=200 )
	country = CountryField(multiple=False)
	zip_code = models.CharField(max_length=200 )
	#same_shipping_address = models.CharField(max_length=200 )
	#save_info = models.CharField(max_length=200 )
	#payment_option = models.CharField(max_length=200 )
	def __str__(self):
		return self.customer.user.username	

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




class Order(models.Model):
	STATUS= (
		('Pending', 'Pending'),
		('Out for Delivery', 'Out for delivery'),
		('Delivered', 'Delivered'),
		)
	customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
	ref_code = models.CharField(max_length=20)
	product = models.ManyToManyField(OrderItem)
	date_created = models.DateTimeField(auto_now_add= True, null=True )
	status = models.CharField(max_length=200, null=True, choices=STATUS, default='Pending')
	is_ordered= models.BooleanField(default=False, null=True, blank=False)
	billing_address = models.ForeignKey(BillingAddress, on_delete=models.SET_NULL, null=True, blank=True)
	amount = models.FloatField( default=100)
	coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, null=True, blank=True)
	refund_requested=models.BooleanField(default=False)
	refund_granted= models.BooleanField(default=False)
	#amount = models.ForeignKey( Payment, on_delete=models.SET_NULL, null=True, blank=True)
	

	"""docstring for Order"""
	def __str__(self):
		return self.customer.name


# not working 

	def get_total(self):
		total = 0
		for order_item in self.product.all():
			total += order_item.get_final_price()
		if self.coupon:
			total -= self.coupon.amount
		return total 


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
	
