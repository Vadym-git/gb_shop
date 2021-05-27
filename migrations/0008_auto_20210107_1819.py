# Generated by Django 3.1.3 on 2021-01-07 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_auto_20210107_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accuser',
            name='acc_link',
            field=models.CharField(max_length=250, unique=True, verbose_name='acceptance link'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone_number',
            field=models.CharField(max_length=17, verbose_name='Phone number'),
        ),
    ]