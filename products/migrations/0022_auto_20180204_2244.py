# Generated by Django 2.0 on 2018-02-04 20:44

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0021_auto_20180204_2243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='cart',
            field=models.BooleanField(default=False, verbose_name=products.models.Cart),
        ),
    ]
