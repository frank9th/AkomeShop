from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


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

class ClientCodeForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(
        attrs={
        'placeholder': 'Enter Clients Code ',
        'class':'form-control',
        }))

class ClientCheckOutForm(forms.Form):
    additional_note = forms.CharField(required=False, widget=forms.Textarea(
        attrs={
        'placeholder': 'Enter any additional infor or message',
        'class':'form-control',
        'rows':3
        }))
    
    payment_option = forms.ChoiceField(widget=forms.RadioSelect(), choices=PAYMENT_CHOICES)
