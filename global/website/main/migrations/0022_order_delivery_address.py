# Generated by Django 5.0.4 on 2024-05-25 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_orderitem_ingredients'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_address',
            field=models.CharField(default='', max_length=100),
        ),
    ]