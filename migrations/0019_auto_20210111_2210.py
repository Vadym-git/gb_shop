# Generated by Django 3.1.3 on 2021-01-11 22:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0018_auto_20210109_2013'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='curtproduct',
            name='curt_id',
        ),
        migrations.RemoveField(
            model_name='curtproduct',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='curtproduct',
            name='product',
        ),
        migrations.DeleteModel(
            name='Curt',
        ),
        migrations.DeleteModel(
            name='CurtProduct',
        ),
    ]
