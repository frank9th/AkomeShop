from django.conf import settings
from django.db import models
from django.shortcuts import reverse 
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from store.models import * 
from django.db.models import Sum
# Create your models here.

class Client(models.Model):
	title = models.CharField(max_length=200, null=True, blank=True)
	full_name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True, blank=True)
	phone1 = models.CharField(max_length=200, null=True )
	phone2 = models.CharField(max_length=200, null=True, blank=True )
	town = models.CharField(max_length=200, null=True)
	apartment_address = models.CharField(max_length=200, null=True, )
	land_mark = models.CharField(max_length=200, null=True )
	client_code = models.CharField(max_length=10, null=True)
	agent_code = models.CharField(max_length=10, null=True, blank=True)
	sex = models.CharField(max_length=70, null=True )
	date_created = models.DateTimeField(auto_now_add= True, null=True )
	image = models.ImageField(upload_to='profile/cover/', null=True, blank=True)


	def __str__(self):
		return self.client_code 


class Agent(models.Model):
	info = models.ForeignKey('Client', on_delete=models.SET_NULL, null=True, blank=True )
	zone = models.CharField(max_length=200, null=True, blank=True )
	agent_code = models.CharField(max_length=10, null=True, blank=True, default=101)
	agent_type = models.CharField(max_length=50, blank=True, null=True,)
	bike = models.BooleanField(default=False)
	keke = models.BooleanField(default=False)
	car = models.BooleanField(default=False)

	def __str__(self):
		return f"{self.agent_code } |  {self.zone}"



class ItemTags(models.Model):
	name = models.CharField(max_length=200, null=True, blank=True)

	def __str__(self):
		return self.name


class VendorItem(models.Model):
	title = models.CharField(max_length=200, null=True, blank=True)
	tag = models.ManyToManyField('ItemTags')
	amount = models.FloatField()
	image = models.ImageField(blank=True, null=True)

	def __str__(self):
		return self.title


class Vendor(models.Model):
	info = models.ForeignKey('Client', on_delete=models.SET_NULL, null=True, blank=True)
	business_name = models.CharField(max_length=200, null=True)
	#product_name = models.CharField(max_length=200, null=True)
	product = models.ForeignKey('VendorItem', on_delete=models.SET_NULL, null=True, blank=True)
	goods = models.BooleanField(default=False)
	services = models.BooleanField(default=False)
	skill = models.BooleanField(default=False)
	date_created = models.DateTimeField(auto_now_add= True )
	vendor_code = models.CharField(max_length=10, null=True, blank=True, default=102)
	agent_code = models.ForeignKey('Agent', on_delete=models.SET_NULL, null=True, blank=True)


	def __str__(self):
		return self.vendor_code


class Vpayment(models.Model):
	seller = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True)
	ref_code = models.CharField(max_length=20, blank=True, null=True)
	amount = models.FloatField()
	timestamp = models.DateTimeField(auto_now_add=True)
	paid = models.BooleanField(default=False)

	def __str__(self):
		return self.ref_code


	@property
	def get_total_pay(self):
		payment = self.vpayment_set.all()
		total = sum([self.amount for amount in vpayments])
		return total


class Contact(models.Model):
	sender = models.CharField(max_length=200 )
	phone = models.IntegerField()
	text = models.CharField(max_length=200)

	def __str__(self):
		return self.sender 












