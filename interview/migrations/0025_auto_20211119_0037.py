# Generated by Django 3.1.7 on 2021-11-19 00:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('interview', '0024_feedback'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='feedback',
            options={'verbose_name': 'Обратная связь', 'verbose_name_plural': 'Обратные связи'},
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField(blank=True, null=True, verbose_name='Курсы')),
                ('profession', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interview.profession')),
            ],
            options={
                'verbose_name': 'Ссылка на курс',
                'verbose_name_plural': 'Ссылки на курсы',
                'db_table': 'courses',
            },
        ),
    ]
