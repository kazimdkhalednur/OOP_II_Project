from django import template

from ..models import Cart

register = template.Library()


@register.filter
def cart_count(user):
    if user.is_authenticated:
        return Cart.objects.filter(user=user).count()
    return 0
