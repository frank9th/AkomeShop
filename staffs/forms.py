from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from django import forms 
from django.forms import ModelForm
from .models import * 
from store.models import *
class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']


CATHEGORY = (
		('G', 'Goods'),
		('S', 'Services')
		)
class OrderForm(forms.Form):
	cathegory =  forms.ChoiceField(widget=forms.RadioSelect(), choices=CATHEGORY)
	name = forms.CharField(widget=forms.TextInput(
		attrs={
		'placeholder': 'Enter item/service name ',
		'class':'form-control '
		}))
	price = forms.IntegerField(widget=forms.NumberInput(
		attrs={
		'placeholder': 'Enter amount ',
		'class':'form-control '
		}))
	description = forms.CharField(widget=forms.TextInput(
		attrs={
		'placeholder': 'additional note/description  ',
		'class':'form-control'
		}))
	
	#slug = models.SlugField()


class UpdateOrderForm(ModelForm):
	class Meta:
		model = Order
		fields = '__all__'



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
	agent_code = forms.CharField(required=False, widget=forms.TextInput(
		attrs={
		'placeholder': 'Re Enter Code',
		'class':'form-control py-0'
		}))
	phone1 = forms.CharField(widget=forms.TextInput(
		attrs={
		'placeholder': 'Enter mobile number',
		'class':'form-control'
		}))
	phone2 = forms.CharField(required=False, widget=forms.TextInput(
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
	sex = forms.CharField(widget=forms.TextInput(
		attrs={
		'placeholder': 'Male/Female',
		'class':'form-control'
		}))
	

class AddVendorForm(forms.Form):
	BUS_CHOICES=(
		('G', 'Goods'),
		('S', 'Services'),
		('Sk', 'Skill'),
		)
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
	agent_code = forms.CharField(required=False, widget=forms.TextInput(
		attrs={
		'placeholder': 'Enter Agent Code ',
		'class':'form-control',
		'name':'agentId',
		'id':'agentId',
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
	zone = forms.CharField(widget=forms.TextInput(
		attrs={
		'placeholder': 'Town/city',
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
class DeliveryForm(forms.Form):
	ref_code = forms.CharField(widget=forms.TextInput(
		attrs={
		'placeholder': 'Enter Client id',
		'class':'form-control',
		'aria-label':'Recipient\'s username', 
		'aria-describedby':'basic-addon2'
		}))

class CodeForm(forms.Form):
	code = forms.CharField(widget=forms.TextInput(
		attrs={
		'placeholder': 'Enter Agent id',
		'class':'form-control',
		'aria-label':'Recipient\'s username', 
		'aria-describedby':'basic-addon2'
		}))


class ContactForm(forms.ModelForm):
	class Meta:
		model = Contact
		fields = '__all__'
		widgets = {
			'sender' : forms.TextInput(
				attrs={
				'id': 'senderId', 
		        'required': True, 
		        'placeholder': 'Enter sender\'s name ',
		        'class':'form-control',
				}),
			'phone' : forms.TextInput(
				attrs={
				'id': 'phoneId', 
		       'placeholder': 'Enter mobile number',
				'class':'form-control',
				}),
			'text': forms.Textarea(attrs={
				'id': 'textId', 
		        'rows': 4,
		        'class':'form-control',
		        'placeholder': 'Say something...',
		    }),


		}

	 