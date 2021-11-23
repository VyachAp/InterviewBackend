# Generated by Django 3.1.7 on 2021-11-23 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interview', '0025_auto_20211119_0037'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='name',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Название компании'),
        ),
        migrations.AlterField(
            model_name='course',
            name='link',
            field=models.URLField(blank=True, null=True, verbose_name='Ссылка'),
        ),
    ]