# Generated by Django 3.1.3 on 2021-01-07 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_accuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accuser',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
