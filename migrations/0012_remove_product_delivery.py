# Generated by Django 3.1.3 on 2021-01-08 17:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_order_delivery'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='delivery',
        ),
    ]
