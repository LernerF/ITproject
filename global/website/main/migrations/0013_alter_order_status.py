# Generated by Django 5.0.4 on 2024-05-20 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Готовится', 'Готовится'), ('on_the_way', 'В пути'), ('completed', 'Завершен')], default='preparing', max_length=20),
        ),
    ]
