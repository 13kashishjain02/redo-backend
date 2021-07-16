# Generated by Django 3.2 on 2021-07-16 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_order_previous_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='is_done',
        ),
        migrations.AlterField(
            model_name='order',
            name='landmark',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
