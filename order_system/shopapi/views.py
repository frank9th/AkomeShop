from django.shortcuts import render
import json
import requests
from rest_framework import viewsets 
from store.models import *
from staffs.models import *
from .serializers import *
from rest_framework.decorators import action

class VpayView(viewsets.ModelViewSet): 
	queryset = Vpayment.objects.all()
	serializer_class = VpaySerializer

class ClientView(viewsets.ModelViewSet): 
	queryset = Client.objects.all()
	serializer_class = ClientSerializer

class VendorView(viewsets.ModelViewSet): 
	queryset = Vendor.objects.all()
	serializer_class = VendorSerializer
