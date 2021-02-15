
from django.conf import settings
from django.db import models
from django.shortcuts import reverse 
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from store.models import * 

# Create your models here.

class Agent(models.Model):
	full_name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True )
	phone1 = models.IntegerField(null=True )
	phone2 = models.IntegerField(null=True, blank=True )
	town = models.CharField(max_length=50)
	address = models.CharField(max_length=200, null=True )
	address = models.CharField(max_length=200, null=True )
	agent_id = models.CharField(max_length=50, blank=True)
	agent_type = models.CharField(max_length=50, blank=True)
	bike = models.BooleanField(default=False)
	keke = models.BooleanField(default=False)
	car = models.BooleanField(default=False)
	

	def __str__(self):
		return self.full_name

class Client(models.Model):
	title = models.CharField(max_length=200, null=True, blank=True)
	full_name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True, blank=True)
	phone1 = models.CharField(max_length=200, null=True )
	phone2 = models.CharField(max_length=200, null=True, blank=True )
	town = models.CharField(max_length=200, null=True)
	address = models.CharField(max_length=200, null=True )
	client_id = models.CharField(max_length=50, null=True, blank=True )
	agent_id = models.CharField(max_length=10, null=True)
	sex = models.CharField(max_length=70, null=True )
	date_created = models.DateTimeField(auto_now_add= True, null=True )


	def __str__(self):
		return self.full_name 

class Vendor(models.Model):

	'''
	SEX= (
		('male', 'Male'),
		('female', 'Female')
		)
	CATHEGORY= (
		('goods', 'Goods/Product'),
		('service', 'Services'),
		('fast food ', 'Fast Food')
		)

	'''
	first_name = models.CharField(max_length=200, null=True)
	last_name  = models.CharField(max_length=200, null=True)
	sex  = models.CharField(max_length=200, null=True)
	email  = models.CharField(max_length=200, null=True)
	apartment_address = models.CharField(max_length=200, null=True)
	street_address  = models.CharField(max_length=200, null=True)
	phone1 = models.CharField(max_length=200, null=True)
	phone2= models.CharField(max_length=200, null=True)
	business_name = models.CharField(max_length=200, null=True)
	product_name = models.CharField(max_length=200, null=True)
	goods = models.BooleanField(default=False)
	services = models.BooleanField(default=False)
	skill = models.BooleanField(default=False)
	date_created = models.DateTimeField(auto_now_add= True, null=True )
	vendor_id = models.CharField(max_length=10, null=True, blank=True)
	agent_id = models.CharField(max_length=10, null=True, blank=True)

	def __str__(self):
		return self.first_name 




