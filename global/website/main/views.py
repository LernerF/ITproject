from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login
from django.views import View
from django.contrib.auth import logout
from django.http import JsonResponse
from .models import Pizza, Cart, CartItem

def index(request):
    return render(request, 'main/index.html')

def main_menu(request):
    return render(request, 'main/menu.html')

def about(request):
    return render(request, 'main/about.html')

def test_login(request):
    return render(request, 'main/test_login.html')

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
