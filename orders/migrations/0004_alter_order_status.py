# Generated by Django 5.0.4 on 2024-04-17 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0003_rename_address2_order_address_2"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Pending"),
                    ("cancelled", "Cancelled"),
                    ("paid", "Paid"),
                    ("shipped", "Shipped"),
                    ("delivered", "Delivered"),
                    ("returned", "Returned"),
                    ("refunded", "Refunded"),
                ],
                default="pending",
                max_length=15,
            ),
        ),
    ]
