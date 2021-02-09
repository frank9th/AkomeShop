from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from django import forms 
from django.forms import ModelForm
from .models import * 

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']


class AddClientForm(forms.Form):
	title = forms.CharField(widget=forms.TextInput(
		attrs={
		'placeholder': 'Mr./Mrs./Master/Miss.',
		'class':'form-control'
		}))
	full_name = forms.CharField(widget=forms.TextInput(
		attrs={
		'placeholder': 'Enter client\'s name',
		'class':'form-control py-0'
		}))
	email = forms.CharField(required=False, widget=forms.TextInput(
		attrs={
		'placeholder': 'Enter email',
		'class':'form-control py-0'
		}))
	phone = forms.CharField(widget=forms.TextInput(
		attrs={
		'placeholder': 'Enter mobile number',
		'class':'form-control'
		}))
	town = forms.CharField(widget=forms.TextInput(
		attrs={
		'placeholder': 'Enter town/city name ',
		'class':'form-control'
		}))
	land_mark = forms.CharField(widget=forms.TextInput(
		attrs={
		'placeholder': 'Enter Nearest land mark',
		'class':'form-control'
		}))
	apartment_address = forms.CharField(widget=forms.TextInput(
		attrs={
		'placeholder': 'Enter Home Address',
		'class':'form-control'
		}))
	agent_id = forms.CharField(widget=forms.TextInput(
		attrs={
		'placeholder': 'Enter Agent ID',
		'class':'form-control'
		}))
	

"""

	full_name = 
	email = 
	phone = 
	town =
	address = 
	client_id = 
	occupation = 
	sex =
"""

class AddVendorForm(forms.Form):
	BUS_CHOICES=(
		('G', 'Goods'),
		('S', 'Services'),
		('Sk', 'Skill'),

		)
	first_name = forms.CharField(widget=forms.TextInput( attrs={
		'placeholder': 'Enter first name',
		'class':'form-control py-0',
			}))
	last_name = forms.CharField(widget=forms.TextInput(
		attrs={
		'placeholder': 'Enter last name',
		'class':'form-control py-0',
			}))
	sex = forms.CharField(required=False, widget=forms.TextInput(
		attrs={
		'placeholder': 'Male or Female ',
		'class':'form-control',
			}))#custom-select d-block w-100
	email = forms.CharField(widget=forms.TextInput(
		attrs={
		'placeholder': 'Enter Email ',
		'class':'form-control',
			}))
	
	apartment_address = forms.CharField(widget=forms.TextInput(
		attrs={
		'placeholder': 'Apartment/businees Address',
		'class':'form-control',
			}))
	street_address = forms.CharField(widget=forms.TextInput(
		attrs={
		'placeholder': '1234 Main St',
		'class':'form-control'
		}))
	phone1 =  forms.CharField(widget=forms.TextInput(
		attrs={
		'placeholder': 'Telephone  ',
		'class':'form-control',
			}))
	phone2 =  forms.CharField(widget=forms.TextInput(
		attrs={
		'placeholder': 'mobile ',
		'class':'form-control',
			}))
	business_name = forms.CharField(widget=forms.TextInput(
		attrs={
		'placeholder': 'Enter business name ',
		'class':'form-control',
			}))
	product_name = forms.CharField(required=False, widget=forms.TextInput(
		attrs={
		'placeholder': 'Enter Product/service name ',
		'class':'form-control',
			}))
	goods = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
		'class':'custom-checkbox', 
		}))
	services = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
		'class':'custom-checkbox'
		}))
	skill = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
		'class':'custom-checkbox', 
		}))

	"""
		first_name
		last_name
		sex
		email
		apartment_address
		street_address
		phone1
		phone2
		business_name
		product_name
		goods
		services
		skill


	"""	
AGENT_TYPE =(

		('D', 'Delivery Agent'),
		('FD', 'Field Agent'),
		)
class AddAgentForm(forms.Form):
	full_name = forms.CharField(widget=forms.TextInput( attrs={
		'placeholder': 'Enter full name',
		'class':'form-control py-0',

			}))
	email = forms.CharField(widget=forms.TextInput( attrs={
		'placeholder': 'Enter email',
		'class':'form-control py-0',
			}))
	phone1 = forms.CharField( widget=forms.TextInput(
		attrs={
		'placeholder': 'Telephone  ',
		'class':'form-control',
			}))
	phone2 = forms.CharField(required=False, widget=forms.TextInput(
		attrs={
		'placeholder': 'alternative number  ',
		'class':'form-control',
			}))
	town = forms.CharField(widget=forms.TextInput(
		attrs={
		'placeholder': 'Town/city',
		'class':'form-control'
		}))
	address = forms.CharField(widget=forms.TextInput(
		attrs={
		'placeholder': '1234 Main St',
		'class':'form-control'
		}))
	bike = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
		'class':'custom-checkbox', 
		}))
	keke = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
		'class':'custom-checkbox', 
		}))
	car =forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
		'class':'custom-checkbox', 
		}))
	agent_type = forms.ChoiceField(widget=forms.RadioSelect(), choices=AGENT_TYPE)


'''
	AGENT INFO:
	full_name = 
	email = 
	phone1 = 
	phone2 = 
	town = 
	address = 
	agent_id = 
	bike = 
	keke = 
	car = 

'''
