# Generated by Django 5.0.3 on 2024-05-23 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_alter_cartitem_ingredients'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='ingredients',
            field=models.ManyToManyField(blank=True, to='main.ingredient'),
        ),
    ]
