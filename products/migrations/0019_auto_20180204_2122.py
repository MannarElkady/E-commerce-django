# Generated by Django 2.0 on 2018-02-04 19:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_item_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='count',
            field=models.CharField(default=0, max_length=200),
        ),
        migrations.AlterField(
            model_name='item',
            name='cart',
            field=models.ForeignKey(default=0, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.Cart'),
        ),
    ]
