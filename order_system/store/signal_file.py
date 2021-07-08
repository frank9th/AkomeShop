from store.views import *
from staffs.views import *

from django.core.signals import request_finished
from django.dispatch import receiver, Signal 


from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token




@receiver(request_finished)
def my_callback(sender, **kwargs ):
 	print("Request finished!")



# This allow to create the token signal from the user creation model 
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

