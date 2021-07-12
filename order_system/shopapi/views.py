
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
from rest_framework.decorators import action
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView


'''
class VpayView(viewsets.ModelViewSet): 
	queryset = Vpayment.objects.all()
	serializer_class = VpaySerializer
'''

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def apiOverview(request):
	api_urls = {
	'List users' : 'api/profile/',
	'Single users' : 'api/profile/pk',
	'Detail View' :'/task-detail/<pk>/',
	'Add Client': '/api/add-client/',
	'Create User': '/api/create/account/',
	'Update profile': '/api/profile/update/',
	'Delete Client': 'api/client-delete/<pk>/user/',
	'Clients':'/api/client/data/users/',
	'Client Detail': 'api/client-detail/<pk>/user/',
	'Sellers':'/api/shop/vendor/data/',
	'Order':'/api/shop/order/data/',
	'account-details': 'api/profile/account/<str:pk>/',

	}
	return Response(api_urls)




class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class ExampleView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
    	#auth = Token.objects.get(user=request.user)
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)





class ListUsers(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter






# Get all users Api view 
@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def AllUserProfile(request): 
	user_profile = UserProfile.objects.all()
	serializer = AllUserSerializer(user_profile, many=True)
	return Response(serializer.data)





# Get all Single users Api view 
@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def SingleUserProfile(request, code): 
	single_user = UserProfile.objects.get(client_code=code)
	serializer = AllUserSerializer(single_user, many=False)
	return Response(serializer.data)



@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def UserAccountDetails(rquest, pk):
	user = UserAccount.objects.get(id=pk)
	serializer = UserAccountSerializer(user, many=False)
	return Response(serializer.data)
	

# Update/Edit  Client Api 
@api_view(['GET','POST'])
@permission_classes((permissions.IsAuthenticated,))
def UpdateProfile(request, code): 
	#code = request.POST.get('client_code')
	client = UserProfile.objects.get(client_code=code)
	serializer = AllUserSerializer(instance=client, data=request.data)
	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)


class AllUserView(viewsets.ModelViewSet): 
	queryset = UserProfile.objects.all()
	serializer_class = AllUserSerializer





# this Api is to get a single client details by passing in the primary key 
@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def ClientDetail(request, pk): 
	client = Client.objects.get(id=pk)
	serializer = ClientSerializer(client, many=False)
	return Response(serializer.data)



# Create Client Api 
@api_view(['GET','POST'])
@permission_classes((permissions.IsAuthenticated,))
def AddClient(request):
	serializer = UserProfileSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()
	#return Response(serializer.data)
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET','POST'])
@permission_classes((permissions.IsAuthenticated,))
def AddProduct(request):
	serializer = ProductSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





# Update/Edit  Client Api 
@api_view(['GET', 'POST'])
@permission_classes((permissions.IsAuthenticated,))
def ClientUpdate(request, pk): 
	client = Client.objects.get(id=pk)
	serializer = ClientSerializer(instance=client, data=request.data)
	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)

# Delete Client Api 
@api_view(['DELETE'])
@permission_classes((permissions.IsAuthenticated,))
def DeleteClient(request, pk): 
	client = Client.objects.get(id=pk)
	client.delete()
	message.alert("client deleted succesfuly ")

	return render('/api')


class VendorView(viewsets.ModelViewSet): 
	queryset = Seller.objects.all()
	serializer_class = VendorSerializer
	

class ProductView(viewsets.ModelViewSet): 
	queryset = Product.objects.all()
	serializer_class = ProductSerializer




@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def OrderView(request): 
	order = Order.objects.all()
	serializer = OrderSerializer(order, many=True)
	return Response(serializer.data)