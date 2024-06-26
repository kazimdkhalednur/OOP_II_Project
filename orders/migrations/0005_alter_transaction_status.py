# Generated by Django 5.0.4 on 2024-04-17 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0004_alter_order_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="status",
            field=models.CharField(
                choices=[
                    ("PENDING", "Pending"),
                    ("VALID", "VALID"),
                    ("FAILED", "FAILED"),
                    ("CANCELLED", "CANCELLED"),
                    ("UNATTEMPTED", "UNATTEMPTED"),
                    ("EXPIRED", "EXPIRED"),
                    ("REFUNDED", "REFUNDED"),
                ],
                default="PENDING",
                max_length=15,
            ),
        ),
    ]
