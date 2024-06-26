# Generated by Django 5.0.3 on 2024-05-14 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_ingredient_pizza_description_alter_pizza_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pizza',
            name='ingredients',
            field=models.ManyToManyField(blank=True, to='main.ingredient', verbose_name='Ингредиенты'),
        ),
        migrations.AlterField(
            model_name='pizza',
            name='description',
            field=models.TextField(default='Описание пиццы', verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='pizza',
            name='image',
            field=models.ImageField(upload_to='pizza_images', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='pizza',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='pizza',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Цена'),
        ),
    ]
