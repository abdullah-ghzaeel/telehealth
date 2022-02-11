# Generated by Django 4.0.2 on 2022-02-11 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0002_phoneverification"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="address",
            field=models.TextField(blank=True, null=True, verbose_name="Address"),
        ),
        migrations.AddField(
            model_name="user",
            name="name",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="Name"
            ),
        ),
    ]
