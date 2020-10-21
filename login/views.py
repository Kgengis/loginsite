from django.shortcuts import render, redirect
from . import models
from .forms import OrderForm, CreateUserForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group


# Create your views here.

@login_required(login_url='loginuser')
@admin_only
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


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()

    context = {'orders': orders}
    return render(request, 'login/user.html', context)


@login_required(login_url='loginuser')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = models.Product.objects.all()
    return render(request, 'login/products.html', {'products': products})


@unauthenticated_user
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


@unauthenticated_user
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            customer.objects.create(
                user=user,
            )
            messages.success(request, 'Account was created for ' + username)
            return redirect('loginuser')

    context = {'form': form}
    return render(request, 'login/register.html', context)


@login_required(login_url='loginuser')
@allowed_users(allowed_roles=['admin'])
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
@allowed_users(allowed_roles=['admin'])
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
@allowed_users(allowed_roles=['admin'])
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
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = models.Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {
        'item': order,
    }
    return render(request, 'login/delete.html', context)
