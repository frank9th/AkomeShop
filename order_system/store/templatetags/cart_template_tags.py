from django import template
from store.models import Order, Transactions

register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].items.count()
    return 0


@register.filter
def trans_item_count(user):
    if user.is_authenticated:
        qs = Transactions.objects.filter(account=user.useraccount, status='Pending')
        if qs.exists():
         return qs.count()
    return 0

@register.filter
def trans_item(user):
    if user.is_authenticated:
        qs = Transactions.objects.filter(account=user.useraccount, status='Pending').order_by('-time')
        for item in qs:
            print(item.amount)
            print(item.transaction_type)
            return item
    return "No resent notification"
