# Generated by Django 3.1.7 on 2021-05-31 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interview', '0006_account_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='profession',
            name='english_name',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Название на английском'),
        ),
    ]
