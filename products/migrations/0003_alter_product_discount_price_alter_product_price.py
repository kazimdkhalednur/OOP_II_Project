# Generated by Django 5.0.4 on 2024-04-14 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0002_alter_product_category_cart"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="discount_price",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.IntegerField(),
        ),
    ]
