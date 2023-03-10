# Generated by Django 4.1.4 on 2023-01-12 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ModeMenu",
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
                ("sModeName", models.CharField(max_length=6, unique=True)),
                ("sTime", models.DurationField(null=True)),
                ("sPrice", models.FloatField(null=True)),
                ("sPPoint", models.FloatField(null=True)),
                ("sCarbon", models.FloatField(null=True)),
            ],
            options={
                "verbose_name": "洗衣模式價格表",
                "verbose_name_plural": "洗衣模式價格表",
            },
        ),
        migrations.CreateModel(
            name="Store",
            fields=[
                (
                    "sStoreID",
                    models.CharField(max_length=32, primary_key=True, serialize=False),
                ),
                ("sStoreName", models.CharField(max_length=10)),
                ("sStoreAdd", models.CharField(max_length=100)),
            ],
            options={
                "verbose_name": "店鋪",
                "verbose_name_plural": "店鋪",
            },
        ),
    ]
