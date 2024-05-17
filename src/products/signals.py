from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender="products.Product")
def check_price(instance, sender, **kwargs):
    if instance.discount_price < instance.price:
        raise ValidationError({"price": "Discount price must be less than price"})
