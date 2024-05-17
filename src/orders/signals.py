from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Order, Transaction


@receiver(pre_save, sender=Transaction)
def update_transaction(sender, instance, **kwargs):
    if instance.status == "VALID":
        instance.is_paid = True
    elif instance.status == "REFUNDED":
        instance.is_paid = False
        instance.is_refund = True


@receiver(post_save, sender=Transaction)
def update_order_status(sender, instance, created, **kwargs):
    if instance.status == "VALID":
        order = Order.objects.get(id=instance.order_id)
        order.status = Order.OrderStatus.PAID
        order.save(update_fields=["status"])

    elif instance.status == "REFUNDED":
        order = Order.objects.get(id=instance.order_id)
        order.status = Order.OrderStatus.REFUNDED
        order.save(update_fields=["status"])
