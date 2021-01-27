from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse 

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




class Order(models.Model):
	STATUS= (
		('Pending', 'Pending'),
		('Out for Delivery', 'Out for delivery'),
		('Delivered', 'Delivered'),
		)
	customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
	amount = models.FloatField( null=True)
	product = models.ManyToManyField(OrderItem)
	date_created = models.DateTimeField(auto_now_add= True, null=True )
	status = models.CharField(max_length=200, null=True, choices=STATUS, default='Pending')
	is_ordered= models.BooleanField(default=False, null=True, blank=False)

	"""docstring for Order"""
	def __str__(self):
		return self.customer.name