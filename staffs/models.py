
from django.conf import settings
from django.db import models
from django.shortcuts import reverse 
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from store.models import * 

# Create your models here.
class Client(models.Model):
	SEX= (
		('male', 'Male'),
		('female', 'Female'),
		('prefered not to say', 'Prefered not to say')

		)
	full_name = models.CharField(max_length=200, null=True )
	email = models.CharField(max_length=200, null=True )
	phone = models.CharField(max_length=200, null=True )
	address = models.CharField(max_length=200, null=True )
	sex = models.CharField(max_length=200, null=True, choices=SEX)
	date_created = models.DateTimeField(auto_now_add= True, null=True )

	def __str__(self):
		return self.full_name

class Vendor(models.Model):
	SEX= (
		('male', 'Male'),
		('female', 'Female')
		)
	CATHEGORY= (
		('goods', 'Goods/Product'),
		('service', 'Services'),
		('fast food ', 'Fast Food')

		)
	first_name = models.CharField(max_length=200, null=True)
	last_name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True )
	phone = models.CharField(max_length=200, null=True )
	address = models.CharField(max_length=200, null=True )
	sex = models.CharField(max_length=200, null=True, choices=SEX)
	business_name = models.CharField(max_length=200, null=True )
	business_type = models.CharField(max_length=200, null=True, choices=CATHEGORY)
	date_created = models.DateTimeField(auto_now_add= True, null=True )

	def __str__(self):
		return self.first_name



class Item(models.Model):
	client = models.ManyToManyField( Client)
	vendor = models.ManyToManyField(Vendor)
	item = models.CharField(max_length=200, null=True )
	quantity = models.IntegerField(default=1)
	amount= models.FloatField( null=True )
	is_ordered= models.BooleanField(default=False)
	date_created = models.DateTimeField(auto_now_add= True, null=True )
	delivery_charge = models.FloatField( max_length=200, null=True, blank=True)

	def __str__(self):
			return self.item

	@property
	def get_total_price(self):
		return self.amount * self.quantity + self.delivery_charge



class PlacedOrder(models.Model):
	ORDER_STATE= (
		('pending', 'Pending'),
		('delivered', 'Delivered'),
		('out for delivery', 'out for delivery'),
		('cancled', 'Cancled')
		)
	customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
	item = models.ForeignKey(Item, null=True, blank=True, on_delete=models.SET_NULL )
	date_created = models.DateTimeField(auto_now_add= True, null=True )
	status = models.CharField(max_length=200, null=True, choices=ORDER_STATE, default='Pending')

	"""docstring for Order"""
	def __str__(self):
		return self.status

