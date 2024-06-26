# Generated by Django 5.0.4 on 2024-04-13 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[("OW", "Owner"), ("CU", "Customer")],
                default="CU",
                max_length=2,
            ),
        ),
    ]
