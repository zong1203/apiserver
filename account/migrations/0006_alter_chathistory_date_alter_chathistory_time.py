# Generated by Django 4.1.2 on 2023-04-25 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_chathistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chathistory',
            name='Date',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='chathistory',
            name='Time',
            field=models.CharField(max_length=10),
        ),
    ]
