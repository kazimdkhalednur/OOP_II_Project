from uuid import uuid4

from django.db import models

from accounts.models import Information, User
from utils import SSLCommerz


class OrderItem(models.Model):
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.ordered(self.quantity)


class OrderManager(models.Manager):
    def get_user_orders(self, user):
        return self.filter(user=user)

    def pending(self, **kwargs):
        return self.filter(status=Order.OrderStatus.PENDING, **kwargs)


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        CANCELLED = "cancelled", "Cancelled"
        PAID = "paid", "Paid"
        SHIPPED = "shipped", "Shipped"
        DELIVERED = "delivered", "Delivered"
        RECEIVED = "received", "Received"
        RETURNED = "returned", "Returned"
        REFUNDED = "refunded", "Refunded"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    info = models.ForeignKey(
        Information, on_delete=models.SET_NULL, blank=True, null=True
    )
    address = models.CharField(max_length=200, blank=True, null=True)
    address_2 = models.CharField(max_length=200, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    district = models.CharField(max_length=50, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    status = models.CharField(
        max_length=15, choices=OrderStatus.choices, default=OrderStatus.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = OrderManager()

    def __str__(self):
        return f"Order {self.id} - {self.user.email}"

    def get_address(self):
        if self.info:
            return self.info.address
        return self.address

    def get_address_2(self):
        if self.info:
            return self.info.address_2
        return self.address_2

    def get_district(self):
        if self.info:
            return self.info.district
        return self.district

    def get_postal_code(self):
        if self.info:
            return self.info.postal_code
        return self.postal_code


class TransactionManager(models.Manager):
    def pending(self, **kwargs):
        return self.filter(status=Transaction.TransactionStatus.PENDING, **kwargs)

    def valid(self, **kwargs):
        return self.filter(status=Transaction.TransactionStatus.VALID, **kwargs)

    def failed(self, **kwargs):
        return self.filter(status=Transaction.TransactionStatus.FAILED, **kwargs)

    def cancelled(self, **kwargs):
        return self.filter(status=Transaction.TransactionStatus.CANCELLED, **kwargs)

    def unattempted(self, **kwargs):
        return self.filter(status=Transaction.TransactionStatus.UNATTEMPTED, **kwargs)

    def expired(self, **kwargs):
        return self.filter(status=Transaction.TransactionStatus.EXPIRED, **kwargs)

    def refunded(self, **kwargs):
        return self.filter(status=Transaction.TransactionStatus.REFUNDED, **kwargs)


class Transaction(models.Model):
    class TransactionStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        VALID = "VALID", "VALID"
        FAILED = "FAILED", "FAILED"
        CANCELLED = "CANCELLED", "CANCELLED"
        UNATTEMPTED = "UNATTEMPTED", "UNATTEMPTED"
        EXPIRED = "EXPIRED", "EXPIRED"
        REFUNDED = "REFUNDED", "REFUNDED"

    # before transaction complete
    id = models.UUIDField(primary_key=True, serialize=True, unique=True, editable=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    status = models.CharField(
        max_length=15,
        choices=TransactionStatus.choices,
        default=TransactionStatus.PENDING,
    )

    # after transaction
    sessionkey = models.CharField(max_length=50, blank=True, null=True)
    gateway_page_url = models.URLField(max_length=300, blank=True, null=True)
    tran_date = models.DateTimeField(blank=True, null=True)
    val_id = models.CharField(max_length=50, blank=True, null=True)
    bank_tran_id = models.CharField(max_length=80, blank=True, null=True)
    store_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    is_paid = models.BooleanField(default=False)
    is_refund = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = uuid4()
        super().save(*args, **kwargs)

    def check_valid_transaction(self):
        ssl_commerz = SSLCommerz()
        return ssl_commerz.validate_payment(self)
