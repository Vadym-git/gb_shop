# Generated by Django 3.1.3 on 2021-01-08 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_auto_20210108_1743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='weight',
            field=models.PositiveIntegerField(default=0, verbose_name='Weight'),
        ),
        migrations.AlterField(
            model_name='product',
            name='weight',
            field=models.PositiveIntegerField(default=0, verbose_name='Weight'),
        ),
    ]
