from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.views import View

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    password_confirmation = models.CharField(max_length=128)
    
    # Добавляем поле корзины для каждого пользователя
    cart = models.OneToOneField('Cart', on_delete=models.CASCADE, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'


class Pizza(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Цена')
    image = models.ImageField(upload_to='media/img', default='../media/img/peperoni.jpeg')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Пицца'
        verbose_name_plural = 'Пиццы'

class Cart(models.Model):
    pizzas = models.ManyToManyField(Pizza, through='CartItem', verbose_name='Пиццы в корзине')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class CartItem(models.Model):
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE, verbose_name='Пицца')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Корзина')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def get_total_price(self):
        return self.pizza.price * self.quantity

    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'
