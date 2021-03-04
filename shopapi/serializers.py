from rest_framework import serializers
from staffs.models import *
from store.models import * 

class VpaySerializer(serializers.ModelSerializer):
	class Meta:
		model = Vpayment
		fields = ('seller', 'ref_code', 'amount', 'paid' )
		#fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
	class Meta:
		model = Client
		fields = ('__all__')

class VendorSerializer(serializers.ModelSerializer):
	class Meta:
		model = Vendor 
		fields = ('__all__')