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

class AccountForm(forms.ModelForm):
	class Meta:
		model =UserProfile
		fields = ['title', 'first_name', 'last_name','email','phone1', 'phone2', 
    	'town', 'apartment_address', 'land_mark', 
    	'agent_code', 'sex']
		widgets = { 
    		'title': forms.TextInput(
				attrs={
				'id': 'titleId', 
		        'required': True, 
		        'placeholder': 'Mr./Mrs./Mis./Dr. ect..',
		        'class':'form-control',
				}), 
    		'first_name':forms.TextInput(
				attrs={
				'id': 'fstId', 
		        'required': True, 
		        'placeholder': 'Enter First Name',
		        'class':'form-control',
				}), 
			'last_name': forms.TextInput(
				attrs={
				'id': 'lstId', 
		        'required': True, 
		        'placeholder': 'Enter last name',
		        'class':'form-control',
				}),  
    		'email': forms.TextInput(
				attrs={
				'id': 'emailId', 
		        'required': False, 
		        'placeholder': 'Enter email',
		        'class':'form-control',
				}), 
    		'phone1':forms.TextInput(
				attrs={
				'id': 'ph1Id', 
		        'required': True, 
		        'placeholder': 'Enter phone number',
		        'class':'form-control',
				}),  
    		'phone2': forms.TextInput(
				attrs={
				'id': 'ph2Id', 
		        'required': False, 
		        'placeholder': 'Enter mobile number',
		        'class':'form-control',
				}), 
    		'town':forms.TextInput(
				attrs={
				'id': 'townId', 
		        'required': True, 
		        'placeholder': 'Town/City',
		        'class':'form-control',
				}),  
    		'apartment_address': forms.TextInput(
				attrs={
				'id': 'aptId', 
		        'required': True, 
		        'placeholder': 'House Address',
		        'class':'form-control',
				}), 
    		'land_mark':forms.TextInput(
				attrs={
				'id': 'landId', 
		        'required': True, 
		        'placeholder': 'Nearest bus stop',
		        'class':'form-control',
				}),  
    		'agent_code': forms.TextInput(
				attrs={
				'id': 'agnId', 
		        'required': False, 
		        'placeholder': 'Agent code(optional)',
		        'class':'form-control',
				}), 
    		'sex':forms.TextInput(
				attrs={
				'id': 'sexId', 
		        'required': False, 
		        'placeholder': 'Male/Female',
		        'class':'form-control',
				}),  
    	
			}


class WalletForm(forms.ModelForm):
	class Meta:
		model = UserAccount
		fields = ['account_name', 'bank_name', 'account_number']
		widgets = {
			'account_name' : forms.TextInput(
				attrs={
				'id': 'accnntId', 
		        'required': True, 
		        'placeholder': 'Enter Account Name  ',
		        'class':'form-control',
				}),
			'bank_name' : forms.TextInput(
				attrs={
				'id': 'bnkId', 
		       'placeholder': 'Enter bank name ',
				'class':'form-control',
				}),
			'account_number': forms.TextInput(attrs={
				'id': 'accnoId', 
		        'class':'form-control',
		        'placeholder': 'Enter Account number',
		    }),


		}



class TopUpForm(forms.Form):
	PAYMENT_CHOICES = (
    ('C', 'Cash'),
    ('CD', 'Card'),
    ('U', 'Ussd'),
	)

	amount = forms.CharField(widget=forms.TextInput(
		attrs={
		'id': 'tpAmtId', 
       'placeholder': 'Enter amount ',
		'class':'form-control',
		}))
	payment_type = forms.ChoiceField(widget=forms.RadioSelect(), choices=PAYMENT_CHOICES)


'''
TODO: add cash out options
1. to bank or 
2. cash 

'''

class TransForm(forms.ModelForm):
	class Meta:
		model = Transaction
		fields = ['account', 'amount', 'note']
		widgets = {
			'account' : forms.TextInput(
				attrs={
				'id': 'actId', 
		        'required': True, 
		        'placeholder': 'Enter Account Name  ',
		        'class':'form-control',
		        'disabled':'',
				}),
			'amount' : forms.TextInput(
				attrs={
				'id': 'amtId', 
		       'placeholder': 'Enter amount ',
				'class':'form-control',
				}),
			'note': forms.Textarea(attrs={
				'id': 'noteId', 
		        'rows': 4,
		        'class':'form-control',
		        'placeholder': 'give reason for your witdrawal',
		    }),


		}

'''
class SavForm(forms.ModelForm):
	class Meta:
		model = Transaction
		fields = ['amount']
		widgets = {
			'amount' : forms.TextInput(
				attrs={
				'id': 'savAmtId', 
		       'placeholder': 'Enter amount ',
				'class':'form-control',
				}),

			}

'''
class SavForm(forms.Form):
	amount = forms.IntegerField(widget=forms.NumberInput(
		attrs={
		'id': 'savAmtId', 
      	'placeholder': 'Enter amount to save ',
		'class':'form-control',
		}))
	duration = forms.IntegerField(widget=forms.NumberInput(
		attrs={
		'id': 'pay_dayId', 
       'placeholder': 'Enter months e.g(3 or 4 ...)',
		'class':'form-control',
		}))




class ConTopUpForm(forms.Form):
	trans_ref = forms.CharField(widget=forms.TextInput(
		attrs={
		'id': 'trns_refId', 
       'placeholder': 'Enter transaction ref code  ',
		'class':'form-control',
		}))
	
class SendMoneyForm(forms.Form):
	amount = forms.IntegerField(widget=forms.NumberInput(
		attrs={
		'id': 'rec_amtId', 
       'placeholder': 'Enter Reciever\'s amount ',
		'class':'form-control',
		}))
	reciever_bank = forms.CharField(widget=forms.TextInput(
		attrs={
		'id': 'rec_bnkId', 
       'placeholder': 'Enter Reciever\'s bank name',
		'class':'form-control',
		}))
	account_name = forms.CharField(widget=forms.TextInput(
		attrs={
		'id': 'rec_accnaId', 
       'placeholder': 'Confirm Reciever\'s account name',
		'class':'form-control',
		}))

class ConfirmAccountForm(forms.Form):
	ACC_TYPE = (
    ('Mek', 'Mek Wallet'),
    ('Other', 'Other Bank')
    )
	account_type =forms.ChoiceField(
   		widget=forms.RadioSelect(),
   		choices=ACC_TYPE)
	account_number = forms.IntegerField(widget=forms.NumberInput(
		attrs={
		'id': 'reciev_accId', 
       'placeholder': 'Enter Reciever\'s account name',
		'class':'form-control',
		}))

'''

class SendMoneyForm(forms.Form):
	ACC_TYPE = (
    ('Mek', 'Mek Wallet'),
    ('Other', 'Other Bank')
    )
	account_type =forms.ChoiceField(
   		widget=forms.RadioSelect(),
   		choices=ACC_TYPE)
	amount = forms.IntegerField(widget=forms.NumberInput(
		attrs={
		'id': 'rec_amtId', 
       'placeholder': 'Enter Reciever\'s amount ',
		'class':'form-control',
		}))
	receiver_name = forms.CharField(widget=forms.TextInput(
		attrs={
		'id': 'rec_naId', 
       'placeholder': 'Enter Reciever\'s Name ',
		'class':'form-control',
		}))
	bank_name = forms.CharField(widget=forms.TextInput(
		attrs={
		'id': 'rec_bnkId', 
       'placeholder': 'Enter Reciever\'s bank name',
		'class':'form-control',
		}))
	account_number = forms.IntegerField(widget=forms.NumberInput(
		attrs={
		'id': 'rec_actkId', 
       'placeholder': 'Enter Reciever\'s account name',
		'class':'form-control',
		}))


'''




"""
Working fields required by serializer update api
"""
{
    "title": " Mrs.",
    "first_name": " Roe(update)",
    "last_name": " Leo",
    "email": " le@gmail.com",
    "phone1": " 09023879",
    "phone2": " ",
    "town": " Jeddo",
    "apartment_address": " merket Rd",
    "land_mark": " Pri Schl",
    "client_code": "TWUJZ",
    "sex": " female",
    "user": 13,
    "agent_code": 1,
    "bus_account": "null",
}


class ClientCodeForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(
        attrs={
        'id':'codeId',
        'placeholder': 'Enter Clients Code ',
        'class':'form-control',   
        }))