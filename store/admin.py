from django.contrib import admin
from .models import * 

def make_refund_accepted(modeladmin, request, queryset):
	queryset.update(refund_requested=False, refund_granted=True )
make_refund_accepted.short_description = 'Update orders to refund granted'

def update_statuse(modeladmin, request, queryset):
	queryset.update(status='Delivered')
update_statuse.short_description = 'Update orders delivered'



class OrderAdmin(admin.ModelAdmin):
	list_display = ['customer', 'is_ordered', 'refund_requested', 'refund_granted', 'status', 'shipping_address', 'amount', 'coupon', 'date_created']
	list_filter = [ 'is_ordered', 'refund_requested', 'refund_granted', 'status']
	list_display_links=['customer','shipping_address', 'amount', 'coupon']
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
