from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginpage, name='loginuser'),
    path('logout/', views.loginpage, name='logout'),
    path('register', views.register, name='register'),
    path('products/', views.products, name='products'),
    path('customer/<str:pk_test>/', views.customer, name='customer'),
    path('createorder/<str:pk>', views.createOrder, name='create_order'),
    path('updateorder/<str:pk>/', views.updateOrder, name='update_order'),
    path('deletaorder/<str:pk>/', views.deleteOrder, name='delete_order'),
]