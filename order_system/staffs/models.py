from django.conf import settings
from django.db import models
from django.shortcuts import reverse 
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from store.models import * 
from django.db.models import Sum
# Create your models here.

class Agent(models.Model):
	#info = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True )
	zone = models.CharField(max_length=200, null=True, blank=True )
	agent_code = models.CharField(max_length=10, null=True, blank=True, default=101)
	agent_type = models.CharField(max_length=50, blank=True, null=True,)
	bike = models.BooleanField(default=False)
	keke = models.BooleanField(default=False)
	car = models.BooleanField(default=False)

	def __str__(self):
		return f"{self.agent_code } |  {self.zone}"


class Vendor(models.Model):
	#info = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True)
	business_name = models.CharField(max_length=200, null=True)
	goods = models.BooleanField(default=False)
	services = models.BooleanField(default=False)
	skill = models.BooleanField(default=False)
	date_created = models.DateTimeField(auto_now_add= True )
	vendor_code = models.CharField(max_length=10, null=True, blank=True, default=102)
	agent_code = models.ForeignKey('Agent', on_delete=models.SET_NULL, null=True, blank=True)
	ref_code = models.CharField(max_length=20, blank=True, null=True)
	amount = models.FloatField()
	paid = models.BooleanField(default=False)


	def __str__(self):
		return self.vendor_code
	@property
	def get_total_pay(self):
		payment = self.vendor_set.all()
		total = sum([self.amount for amount in vendors])
		return total


class Contact(models.Model):
	sender = models.CharField(max_length=200 )
	phone = models.IntegerField()
	text = models.TextField()

	def __str__(self):
		return self.sender 












