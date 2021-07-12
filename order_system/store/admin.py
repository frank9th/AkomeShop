from django.contrib import admin

from .models import *


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'status',
                    'received',
                    'refund_requested',
                    'refund_granted',
                    'shipping_address',
                    'billing_address',
                    'payment',
                    'coupon',
                    'vpaid',
                    ]
    list_display_links = [
        'user',
        'shipping_address',
        'billing_address',
        'payment',
        'coupon'
    ]
    list_filter = ['ordered',
                   'status',
                   'received',
                   'refund_requested',
                   'vpaid',
                   'refund_granted']
    search_fields = [
        'user__username',
        'ref_code'
    ]
    actions = [make_refund_accepted]


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'apartment_address',
        'country',
        'zip',
        'address_type',
        'default'
    ]
    list_filter = ['default', 'address_type', 'country']
    search_fields = ['user', 'street_address', 'apartment_address', 'zip']


admin.site.register(Item)
admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Refund)
admin.site.register(Address, AddressAdmin)
admin.site.register(UserProfile)
admin.site.register(UserAccount)
admin.site.register(Seller)
admin.site.register(Transaction)

admin.site.register(TopupConfirm)
admin.site.register(SendHistory)
admin.site.register(Saving)
admin.site.register(Category)
admin.site.register(Reviews)
admin.site.register(Expensis)
#admin.site.register(Food)
#admin.site.register(FastFood)









'''

from django.contrib import admin
from .models import * 

def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True )
make_refund_accepted.short_description = 'Update orders to refund granted'

def update_statuse(modeladmin, request, queryset):
    queryset.update(status='Delivered')
update_statuse.short_description = 'Update orders delivered'



class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'is_ordered', 'refund_requested', 'refund_granted', 'status', 'client_id', 'amount', 'coupon', 'date_created']
    list_filter = [ 'is_ordered', 'refund_requested', 'refund_granted', 'status']
    list_display_links=['customer','client_id', 'amount', 'coupon']
    search_fields = ['customer__name', 'ref_code' ]

    actions = [make_refund_accepted, update_statuse]

admin.site.register(Customer)
admin.site.register(Tag)
admin.site.register(MallProduct)
admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Address)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Refund)
admin.site.register(Confirmed)
'''

