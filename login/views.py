from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models
from .forms import OrderForm


# Create your views here.

def home(request):
    customers = models.Customer.objects.all()
    orders = models.Order.objects.all()
    total_customer = customers.count()
    total_order = orders.count()

    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {
        'customer': customers,
        'orders': orders,
        'total_order': total_order,
        'delivered': delivered,
        'pending': pending,
    }
    return render(request, 'login/dashboard.html', context)


def products(request):
    products = models.Product.objects.all()
    return render(request, 'login/products.html', {'products': products})


def customer(request, pk_test):
    customer = models.Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    total_order = orders.count()
    context = {
        'customer': customer,
        'orders': orders,
        'total_order': total_order,
    }
    return render(request, 'login/customer.html', context)


def createOrder(request):
    form = OrderForm
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {
        'form': form,
    }
    return render(request, 'login/createOrder.html', context)


def updateOrder(request, pk):
    order = models.Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {
        'form': form,
    }
    return render(request, 'login/createOrder.html', context)


def deleteOrder(request, pk):
    order = models.Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return  redirect('/')

    context = {
        'item': order,
    }
    return render(request, 'login/delete.html', context)
