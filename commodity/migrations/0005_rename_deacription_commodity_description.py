# Generated by Django 4.1.2 on 2023-07-11 02:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('commodity', '0004_commodity_borrowedamount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='commodity',
            old_name='Deacription',
            new_name='Description',
        ),
    ]
