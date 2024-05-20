# Generated by Django 5.0.4 on 2024-05-20 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_order_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('preparing', 'Готовится'), ('on_the_way', 'В пути'), ('completed', 'Завершен')], default='preparing', max_length=20),
        ),
    ]