# Generated by Django 5.0.4 on 2024-04-15 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "products",
            "0005_alter_category_options_alter_product_discount_price_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="is_checked",
            field=models.BooleanField(default=True),
        ),
    ]
