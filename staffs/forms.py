


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from django import forms 
from django.forms import ModelForm
from .models import * 

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']


class CreataOrderForm(ModelForm):
	class Meta:
		model = Item 
		fields = ['client', 'vendor', 'item', 'quantity', 'amount', 'delivery_charge']
	