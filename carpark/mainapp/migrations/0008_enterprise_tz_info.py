# Generated by Django 4.1 on 2022-09-28 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0007_alter_driver_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='enterprise',
            name='tz_info',
            field=models.CharField(default='UTC', max_length=9, verbose_name='Часовой пояс'),
        ),
    ]