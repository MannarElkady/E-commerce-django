# Generated by Django 2.0 on 2018-02-01 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_auto_20180202_0055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='ItemPrice',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='item',
            name='ItemRate',
            field=models.FloatField(default=0.0, max_length=400),
        ),
    ]