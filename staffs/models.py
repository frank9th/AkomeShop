
from django.conf import settings
from django.db import models
from django.shortcuts import reverse 
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from store.models import * 

# Create your models here.

class Client(models.Model):
	title = models.CharField(max_length=200, null=True, blank=True)
	full_name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True, blank=True)
	phone1 = models.CharField(max_length=200, null=True )
	phone2 = models.CharField(max_length=200, null=True, blank=True )
	town = models.CharField(max_length=200, null=True)
	apartment_address = models.CharField(max_length=200, null=True,  )
	land_mark = models.CharField(max_length=200, null=True )
	client_code = models.CharField(max_length=10, null=True)
	agent_code = models.CharField(max_length=10, null=True, blank=True)
	sex = models.CharField(max_length=70, null=True )
	date_created = models.DateTimeField(auto_now_add= True, null=True )

	def __str__(self):
		return self.full_name 


class Agent(models.Model):
	info = models.ForeignKey('Client', on_delete=models.SET_NULL, null=True, blank=True )
	zone = models.CharField(max_length=200, null=True, blank=True )
	agent_code = models.CharField(max_length=10, null=True, blank=True, default=101)
	agent_type = models.CharField(max_length=50, blank=True, null=True,)
	bike = models.BooleanField(default=False)
	keke = models.BooleanField(default=False)
	car = models.BooleanField(default=False)
	

	def __str__(self):
		return f"{self.agent_code } |  {self.zone} zone"


class Vendor(models.Model):
	info = models.ForeignKey('Client', on_delete=models.SET_NULL, null=True, blank=True)
	business_name = models.CharField(max_length=200, null=True)
	product_name = models.CharField(max_length=200, null=True)
	goods = models.BooleanField(default=False)
	services = models.BooleanField(default=False)
	skill = models.BooleanField(default=False)
	date_created = models.DateTimeField(auto_now_add= True )
	vendor_code = models.CharField(max_length=10, null=True, blank=True, default=102)
	agent_code = models.ForeignKey('Agent', on_delete=models.SET_NULL, null=True, blank=True)


	def __str__(self):
		return f"{self.info} | {self.product_name}"




