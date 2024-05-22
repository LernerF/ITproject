from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.views import View
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


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

class Ingredient(models.Model):
    name = models.CharField(max_length=255, verbose_name='Ингредиент')
    is_default = models.BooleanField(default=False, verbose_name='По умолчанию')
    
    def __str__(self):
        return self.name


class Pizza(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    image = models.ImageField(upload_to='pizza_images', verbose_name='Изображение')
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Цена')
    description = models.TextField(verbose_name='Описание', default='Описание пиццы')
    ingredients = models.ManyToManyField('Ingredient', blank=True, verbose_name='Ингредиенты')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Пицца'
        verbose_name_plural = 'Пиццы'



class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    pizzas = models.ManyToManyField(Pizza, through='CartItem', verbose_name='Пиццы в корзине')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class CartItem(models.Model):
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE, verbose_name='Пицца')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Корзина')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    ingredients = models.ManyToManyField(Ingredient, blank=True, verbose_name='Ингредиенты')

    def get_total_price(self):
        return self.pizza.price * self.quantity

    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'

class Order(models.Model):
    STATUS_CHOICES = [
        ('Готовится', 'Готовится'),
        ('В пути', 'В пути'),
        ('Завершен', 'Завершен'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Готовится')

    def __str__(self):
        return f'Order {self.pk} by {self.user.username}'

    def get_total_cost(self):
        return sum(item.get_total_price for item in self.orderitem_set.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.quantity} x {self.pizza.name}'

    @property
    def get_total_price(self):
        return self.quantity * self.pizza.price

