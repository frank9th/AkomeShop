
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from django.shortcuts import render
from rest_framework import status
import json
import requests
from rest_framework import viewsets 
from store.models import *
from staffs.models import *
from .serializers import *
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from rest_framework.response import Response


'''
class VpayView(viewsets.ModelViewSet): 
	queryset = Vpayment.objects.all()
	serializer_class = VpaySerializer
'''

@api_view(['GET'])
def apiOverview(request):
	api_urls = {
	'List users' : '/api/users/account/',
	'Detail View' :'/task-detail/<pk>/',
	'Add Client': '/api/add-client/',
	'Create User': '/api/create/account/',
	'Update Client': '/api/client-update/<pk>/user',
	'Delete Client': 'api/client-delete/<pk>/user/',
	'Clients':'/api/client/data/users/',
	'Client Detail': 'api/client-detail/<pk>/user/',
	'Sellers':'/api/shop/vendor/data/',
	'Order':'/api/shop/order/data/',
	}
	return Response(api_urls)




class UserAccount(viewsets.ModelViewSet): 
	queryset = UserProfile.objects.all()
	serializer_class = UserProfileSerializer

'''
@api_view(['GET'])
def UserList(request): 
	user = UserProfile.objects.all()
	serializer = UserProfileSerializer(user, many=True)
	return Response(serializer.data)
'''


# this Api is to get a single client details by passing in the primary key 
@api_view(['GET'])
def ClientDetail(request, pk): 
	client = Client.objects.get(id=pk)
	serializer = ClientSerializer(client, many=False)
	return Response(serializer.data)




# Create Client Api 
@api_view(['GET','POST'])
def AddClient(request):
	serializer = UserProfileSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()
	#return Response(serializer.data)
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Update/Edit  Client Api 
@api_view(['GET', 'POST'])
def ClientUpdate(request, pk): 
	client = Client.objects.get(id=pk)
	serializer = ClientSerializer(instance=client, data=request.data)
	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)

# Delete Client Api 
@api_view(['DELETE'])
def DeleteClient(request, pk): 
	client = Client.objects.get(id=pk)
	client.delete()
	message.alert("client deleted succesfuly ")

	return render('/api')


class VendorView(viewsets.ModelViewSet): 
	queryset = Vendor.objects.all()
	serializer_class = VendorSerializer



@api_view(['GET'])
def OrderView(request): 
	order = Order.objects.all()
	serializer = OrderSerializer(order, many=True)
	return Response(serializer.data)