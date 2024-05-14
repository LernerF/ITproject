from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm
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
    return render(request, 'main/lkkabinet.html')

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
    
def pizza_list(request):
    pizzas = Pizza.objects.all()
    ingredients = Ingredient.objects.all()
    return render(request, 'main/pizza.html', {'pizzas': pizzas, 'ingredients': ingredients})

@login_required
def add_to_cart_ajax(request, pizza_id):
    if request.method == 'POST':
        try:
            pizza = get_object_or_404(Pizza, pk=pizza_id)
            cart, created = Cart.objects.get_or_create(user=request.user)
            ingredients = request.POST.getlist('ingredients')  # Получаем выбранные ингредиенты
            cart_item, created = CartItem.objects.get_or_create(cart=cart, pizza=pizza)
            if not created:
                cart_item.quantity += 1
                cart_item.save()
            cart_item.ingredients.set(ingredients)  # Устанавливаем выбранные ингредиенты для элемента корзины
            
            # Добавляем описание пиццы к элементу корзины
            cart_item.description = pizza.description
            cart_item.save()
            
            request.session['cart_id'] = cart.pk
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})

    
def remove_from_cart(request, pizza_id):
    pizza = Pizza.objects.get(pk=pizza_id)
    cart = Cart.objects.get(pk=request.session.get('cart_id'))
    cart_item = CartItem.objects.get(cart=cart, pizza=pizza)

    action = request.POST.get('action')
    if action == 'add':
        cart_item.quantity += 1
        cart_item.save()
    elif action == 'subtract':
        cart_item.quantity -= 1
        cart_item.save()
        if cart_item.quantity == 0:
            cart_item.delete()
    return redirect('cart')

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
    