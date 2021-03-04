from store.views import *
from staffs.views import *

from django.core.signals import request_finished
from django.dispatch import receiver, Signal 

@receiver(request_finished)
def my_callback(sender, **kwargs ):
 	print("Request finished!")



