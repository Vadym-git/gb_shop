# Generated by Django 3.1.3 on 2021-01-07 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_auto_20210107_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone_number',
            field=models.BigIntegerField(verbose_name='Phone number'),
        ),
    ]
