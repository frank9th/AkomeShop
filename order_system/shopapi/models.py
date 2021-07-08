from django.db import models

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


# this is to create token for already created useres 
#for user in User.objects.all():
    #Token.objects.get_or_create(user=user)