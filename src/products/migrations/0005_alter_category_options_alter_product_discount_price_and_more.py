# Generated by Django 5.0.4 on 2024-04-15 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0004_cart_is_checked"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={"verbose_name_plural": "Categories"},
        ),
        migrations.AlterField(
            model_name="product",
            name="discount_price",
            field=models.IntegerField(default=566, verbose_name="Price"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.IntegerField(blank=True, verbose_name="Discount Price"),
        ),
    ]
