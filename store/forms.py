from django.forms import ModelForm
from django import forms 
from .models import *
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

class OrderForm(forms.Form):
	class Meta:
		model = Product
		fields = '__all__'

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




class addCustomerForm(ModelForm):
	class Meta:
		model = Customer
		fields = '__all__'



PAYMENT_CHOICES =(

		('S', 'Strip'),
		('P', 'Paypal'),
		('PD', 'Pay on delivery')
		)
class CheckOutForm(forms.Form):
	client_name = forms.CharField(widget=forms.TextInput(
		attrs={
		'placeholder': 'Enter client\'s name',
		'class':'form-control py-0'
		}))
	street_address = forms.CharField(widget=forms.TextInput(
		attrs={
		'placeholder': '1234 Main St',
		'class':'form-control'
		}))
	apartment_address = forms.CharField(required=False, widget=forms.TextInput(
		attrs={
		'placeholder': 'Apartment or suite address',
		'class':'form-control'
		}))
	country = CountryField(blank_label='select country').formfield(widget=CountrySelectWidget(attrs={
		'class':'custom-select d-block w-100'
		}))
	zip_code = forms.CharField(widget=forms.TextInput(
		attrs={
		'placeholder': 'Enter zip code',
		'class':'form-control'
		}))
	same_shipping_address = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
		'class':'custom-checkbox'
		}))
	save_info = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
		'class':'custom-checkbox', 
		}))
	payment_option = forms.ChoiceField(widget=forms.RadioSelect(), choices=PAYMENT_CHOICES)

class CouponForm(forms.Form):
	code = forms.CharField(widget=forms.TextInput(
		attrs={
		'placeholder': 'Promo Code',
		'class':'form-control',
		'aria-label':'Recipient\'s username', 
		'aria-describedby':'basic-addon2'
		}))


class RefundForm(forms.Form):
	ref_code = forms.CharField()
	message = forms.CharField(widget=forms.Textarea(attrs={
		'rows':4 
		}))
	email = forms.EmailField()
