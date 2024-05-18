from django.urls import path
from . import views
from .views import register
from .views import reset_password
from .views import password_change
from .views import UserProfileView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index),
    path('register/', register, name='register'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('login/', views.login_view, name='login'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('logout/', views.logout_view, name='logout'),
    path('pizza/', views.pizza_list, name='pizza_list'),
    path('about/', views.about, name='about'),
    path('test/', views.test_login, name='test_login'),
    path('add_to_cart/<int:pizza_id>/', views.add_to_cart_ajax, name='add_to_cart_ajax'),
    path('remove_from_cart/<int:pizza_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart, name='cart'),
    path('go_to_cart/', views.go_to_cart, name='go_to_cart'),
    path('password_change/<uidb64>/<token>/', views.password_change, name='password_change'),
    path('settings/', views.settings, name='settings'),
    path('order/', views.orders, name='order'),
    path('complete_order/', views.complete_order, name='complete_order'),
    path('order_history/', views.order_history, name='order_history'),
    path('time_place/', views.time_place, name='time_place'),
    #path('submit_order/', views.submit_order, name='submit_order'),
    #path('register-success/', views.registration_success, name='registration-success'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)