from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.views import View
from django.contrib.auth import logout
from django.http import JsonResponse
from .models import Pizza, Cart, CartItem
import os
import smtplib
from django.db.models import Q
from email.mime.text import MIMEText
from email.header    import Header
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formatdate
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem, Pizza, Ingredient
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem, Pizza, Cart, CartItem
from django.utils import timezone
from datetime import timedelta
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError

def index(request):
    return render(request, 'main/index.html')

def main_menu(request):
    return render(request, 'main/menu.html')

def about(request):
    return render(request, 'main/about.html')

def orders(request):
    return render(request, 'main/order.html')

def test_login(request):
    return render(request, 'main/test_login.html')

def reset_password(request):
    return render(request, 'main/reset_password.html')

def reset_password(request):
    return render(request, 'main/change_password.html')

def settings(request):
    return render(request, 'main/settings.html')

def logout_view(request):
    logout(request)
    # После выхода из аккаунта, перенаправляем на другую страницу, например, на главную.
    return redirect('/') 

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            # Создаем пользователя с хэшированным паролем
            User.objects.create_user(username=username, email=email, password=password)
            
            # Перенаправляем на страницу входа
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'main/registration.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.POST.get('next', '/')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(next_url)
        else:
            error_message = "Неправильное имя пользователя или пароль. Пожалуйста, попробуйте снова."
            return render(request, 'main/login.html', {'error_message': error_message, 'next': next_url})

    next_url = request.GET.get('next', '/')
    return render(request, 'main/login.html', {'next': next_url})

def send_email(request, email, url_email, username):
    from django.conf import settings
    subject = 'Восстановление пароля на GalacticPizza'
    message = f"""
    Приветствуем, {username}!

    Ходят слухи, что вы потеряли пароль от GalacticPizza. Если вы и правда запамятовали пароль, придумайте новый, перейдите по ссылке и введите его в соответствующее поле. И никому не говорите!
    {url_email}
    Ваше имя пользователя: {username}
    """
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email,]
    send_mail(subject, message, from_email, recipient_list )

def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # Используем почту вместо имени пользователя 
        user = User.objects.get(email=email)
        username = user.username
        print(user)
        if user is not None:
            url_email = create_token_and_reset_link(user, request)
            send_email(request, email, url_email, username)
    # Если метод запроса не POST, отображаем страницу сброса пароля
    return render(request, 'main/reset_password.html')

def create_token_and_reset_link(user, request):
    # Генерируем токен для пользователя
    token = default_token_generator.make_token(user)

    # Генерируем URL для сброса пароля
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    reset_url = f'{request.build_absolute_uri("/")}password_change/{uid}/{token}'
    print(reset_url)

    return reset_url

@ensure_csrf_cookie
def password_change(request, uidb64, token):
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Проверяем, что пароли совпадают
        if password1 and password2 and password1 == password2:
            try:
                # Декодируем uid из base64
                uid = urlsafe_base64_decode(uidb64).decode()
                user = User.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None

            # Проверяем токен
            if user is not None and default_token_generator.check_token(user, token):
                # Устанавливаем новый пароль
                user.set_password(password1)
                user.save()
                messages.success(request, 'Пароль успешно изменен.')
                return redirect('login')  # Перенаправляем на страницу входа
            else:
                messages.error(request, 'Неверный токен для сброса пароля.')
        else:
            messages.error(request, 'Пароли не совпадают.')

    context = {
        'uidb64': uidb64,
        'token': token,
    }
    return render(request, 'main/password_change.html', context)


class UserProfileView(View):
    def get(self, request):
        # Получаем имя пользователя (логин) и email текущего пользователя
        username = request.user.username
        email = request.user.email

        # Передаем полученные данные в шаблон
        return render(request, 'main/user.html', {'username': username, 'email': email})
    
from django.contrib.auth.decorators import login_required
from django.db.models import Count

@login_required
def pizza_list(request):
    pizzas = Pizza.objects.all()
    ingredients = Ingredient.objects.all()

    # Получение любимых пицц пользователя
    user = request.user
    pizza_counts = (
        OrderItem.objects.filter(order__user=user)
        .values('pizza')
        .annotate(pizza_count=Count('pizza'))
        .order_by('-pizza_count')[:4]
    )
    favorite_pizzas = [Pizza.objects.get(pk=pizza['pizza']) for pizza in pizza_counts]

    return render(request, 'main/pizza.html', {
        'pizzas': pizzas,
        'ingredients': ingredients,
        'favorite_pizzas': favorite_pizzas
    })

@login_required
def add_to_cart_ajax(request, pizza_id):
    if request.method == 'POST':
        try:
            pizza = get_object_or_404(Pizza, pk=pizza_id)
            cart, created = Cart.objects.get_or_create(user=request.user)
            ingredients_ids = request.POST.getlist('ingredients')
            ingredients = Ingredient.objects.filter(id__in=ingredients_ids)

            # Проверка на наличие в корзине аналогичного элемента с теми же убранными ингредиентами
            cart_items = CartItem.objects.filter(cart=cart, pizza=pizza)
            for item in cart_items:
                if set(item.ingredients.all()) == set(ingredients):
                    item.quantity += 1
                    item.save()
                    return JsonResponse({'success': True})

            # Если не найдено, добавляем новый элемент в корзину
            cart_item = CartItem(cart=cart, pizza=pizza)
            cart_item.save()
            cart_item.ingredients.set(ingredients)
            cart_item.save()

            request.session['cart_id'] = cart.pk
            return JsonResponse({'success': True})
        except ValidationError as e:
            return JsonResponse({'success': False, 'error': str(e)})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
    
@login_required
def remove_from_cart(request, pizza_id):
    try:
        pizza = get_object_or_404(Pizza, pk=pizza_id)
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, pizza=pizza)

        action = request.POST.get('action')
        if action == 'add':
            cart_item.quantity += 1
            cart_item.save()
        elif action == 'subtract':
            cart_item.quantity -= 1
            cart_item.save()
            if cart_item.quantity == 0:
                cart_item.delete()

        cart_items = cart.cartitem_set.all()
        total_price = sum(item.get_total_price() for item in cart_items)

        response_data = {
            'success': True,
            'quantity': cart_item.quantity if cart_item.quantity > 0 else 0,
            'item_total_price': cart_item.get_total_price() if cart_item.quantity > 0 else 0,
            'total_price': total_price,
        }
    except Exception as e:
        response_data = {
            'success': False,
            'error': str(e)
        }

    return JsonResponse(response_data)

@login_required
def cart(request):
    try:
        user = request.user
        if user.is_authenticated:
            cart = user.cart
        else:
            cart = Cart.objects.get(pk=request.session.get('cart_id'))
        cart_items = cart.cartitem_set.all()
        total_price = sum(item.get_total_price() for item in cart_items)
        
        # Обновим описание элементов корзины, включая информацию об удаленных ингредиентах
        for item in cart_items:
            if item.ingredients.exists():
                item.description = f"{item.pizza.description} (без {', '.join([ingredient.name for ingredient in item.ingredients.all()])})"
            else:
                item.description = item.pizza.description

        return render(request, 'main/cart.html', {'cart_items': cart_items, 'total_price': total_price})
    except Cart.DoesNotExist:
        cart_items = []
        total_price = 0
    return render(request, 'main/cart.html', {'cart_items': cart_items, 'total_price': total_price})



def go_to_cart(request):
    cart_id = request.session.get('cart_id')
    if cart_id:
        return redirect('cart')
    else:
        return redirect('pizza_list')
"""    
@login_required
def complete_order(request):
    try:
        cart = Cart.objects.get(pk=request.session.get('cart_id'))
        cart_items = cart.cartitem_set.all()
        
        if request.method == 'POST':
            # Создаем новый заказ
            order = Order(user=request.user)
            order.save()

            # Перемещаем все элементы из корзины в заказ
            for item in cart_items:
                order_item = OrderItem(
                    order=order,
                    pizza=item.pizza,
                    quantity=item.quantity,
                    price=item.pizza.price * item.quantity
                )
                order_item.save()
            
            # Очищаем корзину
            cart.cartitem_set.all().delete()
            del request.session['cart_id']  # Удаляем корзину из сессии

            total_cost = order.get_total_cost()
            
            return render(request, 'main/order_complete.html', {'order': order, 'order_items': order.orderitem_set.all(), 'total_cost': total_cost})
        
    except Cart.DoesNotExist:
        return redirect('pizza_list')
    return redirect('cart')
"""

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    order_data = []
    for order in orders:
        items = order.orderitem_set.all()
        item_list = []
        for item in items:
            removed_ingredients = item.ingredients.all()
            removed_ingredients_names = [ingredient.name for ingredient in removed_ingredients]
            item_list.append({
                'pizza_name': item.pizza.name,
                'removed_ingredients': removed_ingredients_names,
                'image_url': item.pizza.image.url,  # Исправлено для получения URL изображения
                'quantity': item.quantity,
                'price': item.pizza.price,
                'total_price': item.quantity * item.pizza.price
            })
        order_data.append({
            'id': order.id,
            'created_at': order.created_at,
            'delivery_time': order.delivery_time,
            'items': item_list,
            'total_cost': order.get_total_cost()
        })
    
    context = {'orders': order_data}
    return render(request, 'main/order_history.html', context)



@login_required
def complete_order(request):
    try:
        cart = Cart.objects.get(pk=request.session.get('cart_id'))
        cart_items = cart.cartitem_set.all()
        
        if request.method == 'POST':
            # Получаем введенное пользователем время доставки
            delivery_time_str = request.POST.get('delivery_time')
            if delivery_time_str:
                # Преобразуем строку времени в объект time
                delivery_time = datetime.strptime(delivery_time_str, '%H:%M').time()
                now = timezone.now()

                # Проверяем, что время доставки не раньше текущего времени
                if delivery_time < now.time():
                    return render(request, 'main/order_error.html', {'error': 'Вы не можете выбрать время доставки раньше текущего времени.'})

            # Создаем новый заказ
            order = Order(user=request.user)
            order.delivery_time = datetime.combine(now.date(), delivery_time)
            order.save()

            # Перемещаем все элементы из корзины в заказ
            for item in cart_items:
                order_item = OrderItem(
                    order=order,
                    pizza=item.pizza,
                    quantity=item.quantity,
                    price=item.pizza.price * item.quantity
                )
                order_item.save()
                # Копируем информацию об убранных ингредиентах
                order_item.ingredients.set(item.ingredients.all())
            
            # Очищаем корзину
            cart.cartitem_set.all().delete()
            del request.session['cart_id']  # Удаляем корзину из сессии

            total_cost = order.get_total_cost()
            
            return render(request, 'main/order_complete.html', {
                'order': order,
                'order_items': order.orderitem_set.all(),
                'total_cost': total_cost,
                'delivery_time': order.delivery_time  # Передаем время доставки в контекст
            })
        
    except Cart.DoesNotExist:
        return redirect('pizza_list')
    return redirect('cart')

@login_required
def time_place(request):
    return render(request, 'main/time_place.html')



def get_order_status(request, order_id):
    # Получаем заказ по его ID
    order = Order.objects.get(pk=order_id)
    # Формируем ответ в формате JSON с актуальным статусом заказа
    data = {
        'status': order.status,
    }
    return JsonResponse(data)