# Generated by Django 5.0.4 on 2024-04-14 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0003_alter_product_discount_price_alter_product_price"),
    ]

    operations = [
        migrations.AddField(
            model_name="cart",
            name="is_checked",
            field=models.BooleanField(default=False),
        ),
    ]
