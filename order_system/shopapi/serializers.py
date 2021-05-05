from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from rest_framework import serializers
from staffs.models import *
from store.models import * 

'''
class VpaySerializer(serializers.ModelSerializer):
	class Meta:
		model = Vpayment
		fields = ('seller', 'ref_code', 'amount', 'paid' )
		#fields = '__all__'
'''



class VendorSerializer(serializers.ModelSerializer):
	class Meta:
		model = Vendor 
		fields = '__all__'



class AllUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserProfile
		fields = ('__all__')


class OrderSerializer(serializers.ModelSerializer):
	class Meta:
		model = Order 
		fields = ('__all__')