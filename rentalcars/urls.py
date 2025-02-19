from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home ,name='home'),
    path('', views.login_view, name='login'),

    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('book/<int:car_id>/', views.book_car, name='book_car'),
    path('payment/<int:booking_id>/', views.payment, name='payment'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('search/', views.search, name='search_cars'),

]
