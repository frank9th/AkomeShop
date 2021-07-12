from django.conf import settings
from django.db import models
#from store.models import * 
#from store.models import UserProfile
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





class Contact(models.Model):
	sender = models.CharField(max_length=200 )
	phone = models.IntegerField()
	text = models.TextField()

	def __str__(self):
		return self.sender 










