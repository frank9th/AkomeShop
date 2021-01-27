from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
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
	name = models.CharField(max_length=200, null=True )
	price = models.FloatField( null=True )
	cathegory = models.CharField(max_length=200, null=True, choices=CATHEGORY)
	description = models.CharField(max_length=200, null=True )
	date_created = models.DateTimeField(auto_now_add= True, null=True )
	tag = models.ManyToManyField(Tag)

	def __str__(self):
		return self.name 



class Order(models.Model):
	STATUS= (
		('Pending', 'Pending'),
		('Out for Delivery', 'Out for delivery'),
		('Delivered', 'Delivered'),
		)
	customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
	price = models.FloatField( null=True)
	product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
	date_created = models.DateTimeField(auto_now_add= True, null=True )
	status = models.CharField(max_length=200, null=True, choices=STATUS, default='Pending')
	is_ordered= models.BooleanField(default=False, null=True, blank=False)

	"""docstring for Order"""
	def __str__(self):
		return self.product.name