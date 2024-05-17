from uuid import uuid4

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone
from tinymce.models import HTMLField

from accounts.models import User

from .utils import slugify


class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name_plural = "Categories"


class ProductManager(models.Manager):
    def published(self, **kwargs):
        return self.filter(status=Product.ProductStatus.PUBLISHED, **kwargs)


class Product(models.Model):
    id = models.UUIDField(
        primary_key=True, blank=True, editable=False, serialize=False, unique=True
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    discount_price = models.IntegerField("Price")
    price = models.IntegerField("Discount Price", blank=True)
    quantity = models.IntegerField()
    thumbnail = models.ImageField(upload_to="products/thumbnails/")
    description = HTMLField()

    class ProductStatus(models.TextChoices):
        DRAFT = "DR", "Draft"
        PUBLISHED = "PB", "Published"
        ARCHIVED = "AR", "Archived"

    status = models.CharField(
        max_length=2,
        choices=ProductStatus.choices,
        default=ProductStatus.DRAFT,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ProductManager()

    def __str__(self) -> str:
        return self.title

    def clean(self):
        if self.discount_price < self.price:
            raise ValidationError({"price": "Discount price must be less than price"})

    def save(self, *args, **kwargs) -> None:
        if not self.id:
            self.id = uuid4()
        self.slug = slugify(self.title)
        if not self.price:
            self.price = self.discount_price
        return super().save(*args, **kwargs)

    def has_inventory(self):
        return self.quantity > 0

    def is_new(self, date=None):
        date = date or timezone.now()
        return (date - self.created_at).days < 30

    def has_discount(self):
        return self.discount_price != self.price

    def get_url(self):
        return reverse("products:detail", kwargs={"slug": self.slug})

    def ordered(self, quantity):
        self.quantity -= quantity
        self.save(update_fields=["quantity"])


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="products/images/")

    def __str__(self) -> str:
        return self.product.title

    def save(self, *args, **kwargs) -> None:
        if ProductImage.objects.filter(product=self.product).count() >= 5:
            raise ValidationError("Only 5 images are allowed per product")
        return super().save(*args, **kwargs)

    @property
    def get_image(self):
        return self.image.url


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="carts")
    quantity = models.IntegerField()
    is_checked = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.user.email} - {self.product.title}"

    def save(self, *args, **kwargs) -> None:
        if not self.user.is_customer():
            raise ValidationError("Owner are not allowed to add products to cart")

        if self.quantity > self.product.quantity:
            raise ValidationError("Quantity exceeds available stock")

        return super().save(*args, **kwargs)

    def get_total(self):
        return self.product.price * self.quantity

    def get_amount_saved(self):
        return (self.product.discount_price * self.quantity) - (
            self.product.price * self.quantity
        )

    def get_add_url(self):
        return reverse("products:cart-add", kwargs={"slug": self.product.slug})

    def get_remove_url(self):
        return reverse("products:cart-remove", kwargs={"slug": self.product.slug})

    def get_delete_url(self):
        return reverse("products:cart-delete", kwargs={"slug": self.product.slug})

    def get_checked_url(self):
        return reverse("products:cart-checked", kwargs={"slug": self.product.slug})
