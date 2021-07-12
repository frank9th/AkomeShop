from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from .models import *

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal'),
    ('PD', 'Pay on delivery'),

)


class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(required=False)
    shipping_address2 = forms.CharField(required=False)
    shipping_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    shipping_zip = forms.CharField(required=False)

    billing_address = forms.CharField(required=False)
    billing_address2 = forms.CharField(required=False)
    billing_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    billing_zip = forms.CharField(required=False)

    same_billing_address = forms.BooleanField(required=False)
    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)
    set_default_billing = forms.BooleanField(required=False)
    use_default_billing = forms.BooleanField(required=False)

    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))


class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    email = forms.EmailField()


class PaymentForm(forms.Form):
    stripeToken = forms.CharField(required=False)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)




CATHEGORY = (
        ('G', 'Goods'),
        ('S', 'Services')
        )

class OrderForm(forms.Form):
    cathegory =  forms.ChoiceField(widget=forms.RadioSelect(), choices=CATHEGORY)
    name = forms.CharField(widget=forms.TextInput(
        attrs={
        'id':'lableId',
        'placeholder': 'Enter item/service name ',
        'class':'form-control '
        }))
    price = forms.IntegerField(widget=forms.NumberInput(
        attrs={
        'id':'priceId',
        'placeholder': 'Enter amount ',
        'class':'form-control '
        }))
    description = forms.CharField(widget=forms.TextInput(
        attrs={
        'id':'descId',
        'placeholder': 'additional note/description',
        'class':'form-control'
        }))
    
    #slug = models.SlugField()



class ClientCheckOutForm(forms.Form):
    additional_note = forms.CharField(required=False, widget=forms.Textarea(
        attrs={
        'id':'noteId',
        'placeholder': 'Enter any additional infor or message',
        'class':'form-control',
        'rows':3
        }))
    
    payment_option = forms.ChoiceField(widget=forms.RadioSelect(
        ),
     choices=PAYMENT_CHOICES)



# TODO: COMPLET THE PRODUCT FORM 

# Product form 
TAG = (
    ('Select', 'Choose tag'),
    ('G', 'Goods'),
    ('S', 'Services'),
    ('FS', 'FastFood')
    )
UNIT = (
    ('YES', 'Yes'),
    ('NO', 'No'),
  
    )

CATEGORY = (
    ('SEL', 'Choose Category'),
    ('Grain', 'Grain'),
    ('Meat', 'Meat'),
    ('Vegetable', 'Vegetable'),
    ('Condiment', 'Condiment'),
    ('Flour', 'Flour'),
    ('Oil', 'Oil'),
    ('Beverage', 'Beverage'),
    ('Fruit', 'Fruit'),
    ('Other', 'Other')
    )

LABEL_CHOICES = (
    ('P', 'Primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)
class ProductForm(forms.Form):
    seller = forms.CharField(widget=forms.TextInput(
        attrs={
        'id':'vendorId',
        'placeholder': 'Enter Number',
        'class':'form-control '
        }))
    title = forms.CharField(widget=forms.TextInput(
        attrs={
        'id':'proNameId',
        'placeholder': 'Product / Service name ',
        'class':'form-control '
        }))
    cost_price = forms.IntegerField(required=False, widget=forms.NumberInput(
        attrs={
        'id':'proPriceId',
        'placeholder': 'Enter market price ',
        'class':'form-control '
        }))
    price = forms.IntegerField(widget=forms.NumberInput(
        attrs={
        'id':'proPriceId',
        'placeholder': 'Enter amount ',
        'class':'form-control '
        }))
    discount_price = forms.IntegerField(required=False, widget=forms.NumberInput(
        attrs={
        'id':'proDiscPriceId',
        'placeholder': 'Enter discount amount ',
        'class':'form-control '
        }))
    short_desc = forms.CharField(widget=forms.Textarea(
        attrs={
        'id':'descId',
        'rows': 2,
        'placeholder': 'Enter short description',
        'class':'form-control'
        }))
    description = forms.CharField(required=False, widget=forms.Textarea(
        attrs={
        'id':'descId',
        'rows': 4,
        'placeholder': 'additional note/description',
        'class':'form-control'
        }))
    image = forms.FileField(required=False,)
    image_two = forms.FileField(required=False,)
    image_three = forms.FileField(required=False,)
    category = forms.ChoiceField(widget=forms.Select(),choices=CATEGORY)
    tag = forms.ChoiceField(widget=forms.Select(),choices=TAG)
    label = forms.ChoiceField(widget=forms.Select(),choices=LABEL_CHOICES)
    unit = forms.ChoiceField(widget=forms.RadioSelect(),choices=UNIT)

    '''
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'title' : forms.TextInput(
                attrs={
                'id':'proNameId',
                'required': True, 
                'placeholder': 'Enter Product/Service name ',
                'class':'form-control',
                }),
            'cost_price' : forms.NumberInput(
                attrs={
                'id': 'costPriceId', 
                'placeholder': 'Enter market price',
                'class':'form-control',
                }),
            'price' : forms.NumberInput(
                attrs={
                'id': 'proPriceId', 
                'placeholder': 'Enter amount',
                'class':'form-control',
                }),
            'discount_price' : forms.NumberInput(
                attrs={
                'id': 'proDicePriceId', 
                'placeholder': 'Enter discount amount',
                'class':'form-control',
                }),
             'short_desc': forms.Textarea(attrs={
                'id': 'shortDectId', 
                'rows': 3,
                'class':'form-control',
                'placeholder': 'Enter short description',
            }),
            'description' : forms.Textarea(attrs={
                'id': 'descId', 
                'rows': 2,
                'class':'form-control',
                'placeholder': 'product/services detail description',
            })

        }

    '''

    
    
    #slug = models.SlugField()
