from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField
from staffs.models import *
import random 
import string 


def create_unique_code():
    return ''.join(random.choices(string.digits, k=10))

client_code = create_unique_code()

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)
    title = models.CharField(max_length=200, null=True, blank=True)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    phone1 = models.CharField(max_length=200, null=True )
    phone2 = models.CharField(max_length=200, null=True, blank=True )
    town = models.CharField(max_length=200, null=True)
    apartment_address = models.CharField(max_length=200, null=True, blank=True)
    land_mark = models.CharField(max_length=200, null=True )
    client_code = models.CharField(max_length=10, null=True)
    agent_code = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True)
    sex = models.CharField(max_length=70, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add= True, null=True )
    is_seller = models.BooleanField(default=False)
    #bus_account = models.ForeignKey(Seller, on_delete=models.SET_NULL, null=True, blank=True)
    is_agent = models.BooleanField(default=False)
    image = models.ImageField(upload_to='profile/cover/', null=True, blank=True)

    def __str__(self):
        return self.user.username

class UserAccount(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    account_name = models.CharField(max_length=200, blank=True, null=True)
    bank_name = models.CharField(max_length=200, blank=True, null=True)
    account_number = models.IntegerField(blank=True, null=True)
    wallet_balance = models.FloatField(default=0.00)
    flex_balance = models.FloatField(default=0.00)
    sav_balance = models.FloatField(default=0.00)

    def __str__(self):
        return self.user.username

def useraccount_receiver(sender, instance, created, *args, **kwargs):
    if created:
        useraccount = UserAccount.objects.create(user=instance)

post_save.connect(useraccount_receiver, sender=settings.AUTH_USER_MODEL)


class Seller(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=200, null=True)
    description = models.TextField()
    town = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    fast_food = models.BooleanField(default=False)
    goods = models.BooleanField(default=False)
    services = models.BooleanField(default=False)
    skill = models.BooleanField(default=False)
    active= models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add= True )
    agent_code = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='cover', blank=True, null=True)

    def __str__(self):
        return self.business_name

    @property
    def get_total_pay(self):
        payment = self.Seller_set.all()
        total = sum([self.amount for amount in vendors])
        return total


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    thubnail= models.ImageField(blank=True, null=True)
    image = models.ImageField(upload_to='product', blank=True, null=True)

    """docstring for Category"""
    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


TAG = (
    ('G', 'Goods'),
    ('S', 'Services'),
    ('FS', 'FastFood')
    )

STAT = (
    ('NEW', 'NEW'),
    ('FREE', 'FREE'),
    ('ON SALE', 'ON SALE'),
    ('NOT ON SALE', 'NOT ON SALE'),
    ('HOT', 'HOT')
    )

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)



# STORE PRODUCTS 
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE )
    seller = models.ForeignKey(UserAccount, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=100)
    cost_price = models.FloatField(blank=True, null=True)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    tag = models.CharField(choices=TAG, max_length=10)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1, default='P')
    status = models.CharField(choices=STAT, max_length=100, default='NEW')
    slug = models.SlugField()
    unit = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    short_desc = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='product', )
    image_two = models.ImageField(upload_to='product', blank=True, null=True)
    image_three = models.ImageField(upload_to='product', blank=True, null=True)


    def __str__(self):
        return self.title 


    def get_absolute_url(self):
        return reverse("store:product", kwargs={
            'slug': self.slug
        })

    def get_category_url(self):
        return reverse("store:product", kwargs={
            'category': self.category.name
        })

    def get_add_to_cart_url(self):
        return reverse("store:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("store:remove-from-cart", kwargs={
            'slug': self.slug
        })


# this model is not yet in use. this may be required later 
class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    #label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField()
    description = models.TextField()
    #image = models.ImageField(blank=True, null=True)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("store:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("store:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("store:remove-from-cart", kwargs={
            'slug': self.slug
        })



class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()



class Order(models.Model):
    STATUS= (
        ('Pending', 'Pending'),
        ('Out for Delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
        )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    client = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, blank=True, null=True)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    note = models.CharField(max_length=200, null=True, blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateField(blank=True, null=True)
    ordered_time = models.TimeField(blank=True, null=True)
    ordered = models.BooleanField(default=False)
    status = models.CharField(max_length=200, null=True, choices=STATUS, default='Pending')
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True )
    received = models.BooleanField(default=False)
    vpaid = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    store_record = models.BooleanField(default=True)

  

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total

    def delivery_charge(self):
        total = self.get_total()
        if total <= 1000:
            delivery_charge = 25
            total = total / 100 * delivery_charge
        elif total <= 2000:
            delivery_charge = 20
            total = total / 100 * delivery_charge 
        elif total <= 5000:
            delivery_charge = 15
            total = total / 100 * delivery_charge 
        elif total >= 5050:
            delivery_charge = 10
            total = total / 100 * delivery_charge 
        return total 
        print(total)

    def ground_total(self):
        return self.delivery_charge() +  self.get_total()
        #print(ground_total)


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    ref_code = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.amount)


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code



class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"



def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance, client_code=client_code)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)


class Transactions(models.Model):
    TRANS_STATUS = (
    ('Debited', 'Debited'),
    ('Credited', 'Credited'),
    ('Pending', 'Pending')
    )

    PAY_TYPE = (
        ('Cash', 'Cash'),
        ('Wallet', 'Wallet'),
        ('Ussd', 'Ussd'),
        ('Online', 'Online')
        )

    TRANS_TYPE = (
    ('Debit', 'Debit'),
    ('Credit', 'Credit'),
    ('Topup', 'Top Up'),
    ('Withdrawal', 'Withdrawal'),
    ('Save', 'Save'),
    ('Send', 'Send')
    )

    transaction_type = models.CharField(choices=TRANS_TYPE, max_length=20)
    payment_type = models.CharField(choices=PAY_TYPE, max_length=10)
    account = models.ForeignKey(UserAccount, on_delete=models.SET_NULL, null=True)
    amount = models.FloatField()
    date = models.DateField()
    time= models.TimeField()
    status = models.CharField( choices=TRANS_STATUS, max_length=10, default='Pending')
    note = models.CharField(max_length=200, null=True, blank=True)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    store_record = models.BooleanField(default=False)

    def __str__(self):
        return self.status


# This is to keep track of who confirm the topup
class TopupConfirm(models.Model):
    approved_by = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    amount = models.FloatField()
    #sender_account = models.CharField(max_length=200, null=True, blank=True)
    trans_ref = models.CharField(max_length=200)

    def __str__(self):
        return self.trans_ref



class SendHistory(models.Model):
    ACC_TYPE = (
    ('Mek', 'Mek Wallet'),
    ('Other', 'Other Bank'),
    )
    sender = models.ForeignKey('UserAccount', on_delete=models.CASCADE)
    account_type = models.CharField(choices=ACC_TYPE, max_length=10)
    amount = models.FloatField()
    account_name = models.CharField(max_length=200)
    account_number = models.CharField(max_length=200)
    bank_name = models.CharField(max_length=200)
    trans_ref = models.CharField(max_length=200)

    def __str__(self):
        return self.account_type


class Saving(models.Model):
    owner = models.ForeignKey('UserAccount', on_delete=models.CASCADE)
    amount = models.FloatField()
    save_date = models.DateField()
    pay_date = models.DateField()
    is_paid = models.BooleanField(default=False)
    ref_code = models.CharField(max_length=30) 

    def __str__(self):
        return str(self.amount)



class Reviews(models.Model):
    name = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name_plural = 'Reviews'


class Expensis(models.Model):
    #sender = models.CharField(max_length=200 )
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    porpurse = models.TextField()
    amount = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.amount 

    class Meta:
        verbose_name_plural = 'Expensis'


class Logistics(models.Model):
    item = models.CharField(max_length=100)
    value_price = models.CharField(max_length=100, null=True, blank=True)
    item_location = models.CharField(max_length=200)
    delivery_address = models.CharField(max_length=200)
    sender_name = models.CharField(max_length=100, null=True, blank=True)
    sender_number = models.IntegerField(null=True, blank=True)
    receiver_name = models.CharField(max_length=100)
    receiver_number = models.IntegerField()
    delivery_charge = models.FloatField()
    ref = models.CharField(max_length=50)
    collect_payment = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    date= models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    note = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.item

    class Meta:
        verbose_name_plural = 'Logistics'



