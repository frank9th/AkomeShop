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



CLASS = (
    ('Big', 'Big'),
    ('Small', 'Small'),
)

class Advert(models.Model):
    title = models.CharField(max_length=200)
    message = models.CharField(max_length=500)
    image = models.ImageField(upload_to='ads', )
    slug= models.SlugField()
    start_date = models.DateField()
    end_date = models.DateField()
    display_section = models.CharField(choices=CLASS, max_length=20)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.title







