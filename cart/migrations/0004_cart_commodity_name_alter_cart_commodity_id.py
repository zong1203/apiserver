# Generated by Django 4.1.2 on 2023-07-09 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_cart_seller'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='Commodity_Name',
            field=models.CharField(default='', max_length=10, verbose_name='購物車內商品名稱'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='Commodity_ID',
            field=models.CharField(max_length=10, verbose_name='購物車內商品ID'),
        ),
    ]
