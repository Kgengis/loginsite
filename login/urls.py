from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginpage, name='loginuser'),
    path('user/', views.userPage, name='user-page'),
    path('logout/', views.logoutuser, name='logout'),
    path('register/', views.register, name='register'),
    path('products/', views.products, name='products'),
    path('customer/<str:pk_test>/', views.customer, name='customer'),
    path('createorder/<str:pk>', views.createOrder, name='create_order'),
    path('updateorder/<str:pk>/', views.updateOrder, name='update_order'),
    path('deletaorder/<str:pk>/', views.deleteOrder, name='delete_order'),
    path('accountsetting/', views.accountSettings, name='accountsetting'),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordChangeDoneView.as_view(), name='password_reset_done'),
    path('reset<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),



]