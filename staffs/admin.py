from django.contrib import admin
from .models import *
from store.models import *

# Register your models here.

admin.site.register(Client)
admin.site.register(Vendor)
admin.site.register(Item)
admin.site.register(PlacedOrder)