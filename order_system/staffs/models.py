from django.conf import settings
from django.db import models
from store.models import * 
from django.db.models import Sum
# Create your models here.

class Agent(models.Model):
	zone = models.CharField(max_length=200, null=True, blank=True )
	agent_code = models.CharField(max_length=10, null=True, blank=True, default=101)
	agent_type = models.CharField(max_length=50, blank=True, null=True,)
	bike = models.BooleanField(default=False)
	keke = models.BooleanField(default=False)
	car = models.BooleanField(default=False)

	def __str__(self):
		return f"{self.agent_code }"


class Vendor(models.Model):
	business_name = models.CharField(max_length=200, null=True)
	description = models.TextField()
	address = models.CharField(max_length=300, null=True, blank=True)
	fast_food = models.BooleanField(default=False)
	goods = models.BooleanField(default=False)
	services = models.BooleanField(default=False)
	skill = models.BooleanField(default=False)
	date_created = models.DateTimeField(auto_now_add= True )
	agent_code = models.ForeignKey('Agent', on_delete=models.SET_NULL, null=True, blank=True)
	image = models.ImageField(upload_to='product', blank=True, null=True)


	def __str__(self):
		return self.business_name
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





class Expensis(models.Model):
	sender = models.CharField(max_length=200 )
	#user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
	porpurse = models.TextField()
	amount = models.IntegerField()

	def __str__(self):
		pass





