# Generated by Django 4.1.4 on 2023-01-11 14:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("OrderApp", "0007_alter_delivery_sdelivery_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="delivery",
            name="sWashTime",
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
