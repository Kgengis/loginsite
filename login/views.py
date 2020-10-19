from django.shortcuts import render, redirect
from . import models
from .forms import OrderForm, CreateUserForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url='loginuser')
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


@login_required(login_url='loginuser')
def products(request):
    products = models.Product.objects.all()
    return render(request, 'login/products.html', {'products': products})


def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password in incorrect')
    context = {}
    return render(request, 'login/login.html', context)


def logoutuser(request):
    logout(request)
    return redirect('loginuser')


@login_required(login_url='loginuser')
def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('loginuser')

        context = {'form': form}
        return render(request, 'login/register.html', context)


@login_required(login_url='loginuser')
def customer(request, pk_test):
    customer = models.Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    total_order = orders.count()
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {
        'customer': customer,
        'orders': orders,
        'total_order': total_order,
        'myFilter': myFilter,
    }
    return render(request, 'login/customer.html', context)


@login_required(login_url='loginuser')
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(models.Customer, models.Order, fields=('product', 'status'))
    customer = models.Customer.objects.get(id=pk)
    formset = OrderFormSet(instance=customer)
    # form = OrderForm(initial={'customer': customer})
    if request.method == 'POST':
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {
        'formset': formset,
    }
    return render(request, 'login/createOrder.html', context)


@login_required(login_url='loginuser')
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


@login_required(login_url='loginuser')
def deleteOrder(request, pk):
    order = models.Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {
        'item': order,
    }
    return render(request, 'login/delete.html', context)
