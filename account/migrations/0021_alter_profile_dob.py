# Generated by Django 3.2.8 on 2022-02-19 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0020_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='dob',
            field=models.DateField(null=True, verbose_name='Date of Birth'),
        ),
    ]
