# Generated by Django 4.1.2 on 2023-04-02 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_userfile_profliephoto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfile',
            name='Password',
            field=models.CharField(max_length=65),
        ),
    ]
