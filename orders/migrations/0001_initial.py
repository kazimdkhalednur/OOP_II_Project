# Generated by Django 5.0.4 on 2024-04-16 14:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("accounts", "0005_remove_information_phone_number_user_phone_number"),
        ("products", "0006_alter_cart_is_checked"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.PositiveIntegerField()),
                ("price", models.PositiveIntegerField()),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.product",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("address", models.CharField(blank=True, max_length=200, null=True)),
                ("address2", models.CharField(blank=True, max_length=200, null=True)),
                ("postal_code", models.CharField(blank=True, max_length=10, null=True)),
                ("district", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PE", "Pending"),
                            ("CA", "Cancelled"),
                            ("PA", "Paid"),
                            ("SH", "Shipped"),
                            ("DE", "Delivered"),
                            ("RE", "Refunded"),
                        ],
                        default="PE",
                        max_length=2,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "info",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="accounts.information",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("items", models.ManyToManyField(to="orders.orderitem")),
            ],
        ),
        migrations.CreateModel(
            name="Transaction",
            fields=[
                (
                    "id",
                    models.UUIDField(primary_key=True, serialize=False, unique=True),
                ),
                ("amount", models.PositiveIntegerField()),
                ("sessionkey", models.CharField(max_length=50)),
                ("gateway_page_url", models.URLField(max_length=300)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PENDING", "Pending"),
                            ("VALID", "VALID"),
                            ("FAILED", "FAILED"),
                            ("CANCELLED", "CANCELLED"),
                            ("UNATTEMPTED", "UNATTEMPTED"),
                            ("EXPIRED", "EXPIRED"),
                        ],
                        default="PENDING",
                        max_length=15,
                    ),
                ),
                ("tran_date", models.DateTimeField(blank=True, null=True)),
                ("val_id", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "bank_tran_id",
                    models.CharField(blank=True, max_length=80, null=True),
                ),
                (
                    "store_amount",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("is_paid", models.BooleanField(default=False)),
                ("is_refund", models.BooleanField(default=False)),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="orders.order"
                    ),
                ),
            ],
        ),
    ]
