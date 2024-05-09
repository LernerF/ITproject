from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login
from django.views import View
from django.contrib.auth import logout
from django.http import JsonResponse
from .models import Pizza, Cart, CartItem
import os
import smtplib
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
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect

def index(request):
    return render(request, 'main/index.html')

def main_menu(request):
    return render(request, 'main/menu.html')

def about(request):
    return render(request, 'main/about.html')

def test_login(request):
    return render(request, 'main/test_login.html')

def reset_password(request):
    return render(request, 'main/reset_password.html')

def reset_password(request):
    return render(request, 'main/change_password.html')


def logout_view(request):
    logout(request)
    # После выхода из аккаунта, перенаправляем на другую страницу, например, на главную.
    return redirect('/') 

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save() 
            login(request, user) 
            return redirect('/') 
    else:
        form = UserRegistrationForm()
    return render(request, 'main/registration.html', {'form': form})

def send_email(request, email, url_email, username):
    subject = 'Восстановление пароля на GalacticPizza'
    message = f"""
    Приветствуем, {username}!

    Ходят слухи, что вы потеряли пароль от GalacticPizza. Если вы и правда запамятовали пароль, придумайте новый, перейдите по ссылке и введите его в соответствующее поле. И никому не говорите!
    {url_email}
    Ваше имя пользователя: {username}
    """
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email,]
    send_mail( subject, message, email_from, recipient_list )

def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # Используем почту вместо имени пользователя 
        user = User.objects.get(email=email)
        username = user.username
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

    return reset_url

from django.views.decorators.csrf import ensure_csrf_cookie

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


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.POST.get('next', '/')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Перенаправляем на главную страницу после успешного входа
            return redirect(next_url)
        else:
            # Возвращаем ошибку, если аутентификация не удалась
            return render(request, 'main/login.html', {'next': next_url, 'invalid_credentials': True})

    # Если метод запроса не POST, отображаем страницу входа
    next_url = request.GET.get('next', '/')
    return render(request, 'main/login.html', {'next': next_url})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.POST.get('next', '/')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Перенаправляем на главную страницу после успешного входа
            return redirect(next_url)
        else:
            # Возвращаем ошибку, если аутентификация не удалась
            return render(request, 'main/login.html', {'next': next_url, 'invalid_credentials': True})

    # Если метод запроса не POST, отображаем страницу входа
    next_url = request.GET.get('next', '/')
    return render(request, 'main/login.html', {'next': next_url})

class UserProfileView(View):
    def get(self, request):
        # Получаем имя пользователя (логин) и email текущего пользователя
        username = request.user.username
        email = request.user.email

        # Передаем полученные данные в шаблон
        return render(request, 'main/user.html', {'username': username, 'email': email})
    
def pizza_list(request):
    pizzas = Pizza.objects.all()
    return render(request, 'main/pizza.html', {'pizzas': pizzas})

def add_to_cart(request, pizza_id):
    pizza = Pizza.objects.get(pk=pizza_id)
    cart, created = Cart.objects.get_or_create(pk=request.session.get('cart_id'))
    cart_item, created = CartItem.objects.get_or_create(cart=cart, pizza=pizza)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    request.session['cart_id'] = cart.pk
    return redirect('pizza_list')

def remove_from_cart(request, pizza_id):
    pizza = Pizza.objects.get(pk=pizza_id)
    cart = Cart.objects.get(pk=request.session.get('cart_id'))
    cart_item = CartItem.objects.get(cart=cart, pizza=pizza)

    action = request.POST.get('action')  # Получаем значение параметра "action"

    if action == 'add':
        print("PABOTAET")
        cart_item.quantity += 1
        cart_item.save()
    elif action == 'subtract':
        cart_item.quantity -= 1
        cart_item.save()  # Сохраняем объект cart_item после изменения количества
        if cart_item.quantity == 0:
            cart_item.delete()
    return redirect('cart')

def cart(request):
    try:
        cart = Cart.objects.get(pk=request.session.get('cart_id'))
        cart_items = cart.cartitem_set.all()
        total_price = sum(item.pizza.price * item.quantity for item in cart_items)
    except Cart.DoesNotExist:
        cart_items = []
        total_price = 0
    return render(request, 'main/cart.html', {'cart_items': cart_items, 'total_price': total_price})


# views.py

def go_to_cart(request):
    cart_id = request.session.get('cart_id')
    if cart_id:
        return redirect('cart')
    else:
        return redirect('pizza_list')
