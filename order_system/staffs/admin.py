from django.contrib import admin
from .models import *
from store.models import *

# Register your models here.

admin.site.register(Client)
admin.site.register(Vendor)
admin.site.register(Agent)
#admin.site.register(VendorItem)
#admin.site.register(ItemTags)
#admin.site.register(Vpayment)
admin.site.register(Contact)
