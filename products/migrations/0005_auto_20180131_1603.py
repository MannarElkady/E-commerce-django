# Generated by Django 2.0 on 2018-01-31 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20180131_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='ItemLogo',
            field=models.ImageField(blank=True, null=True, upload_to='products/'),
        ),
    ]
