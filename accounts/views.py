from django.shortcuts import render, redirect
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views import View
from accounts.models import Product, Order, Customer
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class HomeView(LoginRequiredMixin, View):

    def get(self, request):
        orders = Order.objects.all()
        customers = Customer.objects.all()
        total_customers = customers.count()
        total_orders = orders.count()
        delivered = orders.filter(status='Delivered').count()
        pending = orders.filter(status='Pending').count()
        context = {'orders': orders,
                   'customers': customers,
                   'total_orders': total_orders,
                   'total_customers': total_customers,
                   'delivered': delivered,
                   'pending': pending
                   }
        return render(request, 'accounts/dashboard.html', context)


class ProductView(LoginRequiredMixin, View):

    def get(self, request):
        products = Product.objects.all()
        return render(request, 'accounts/products.html', {'products': products})


class CustomerView(LoginRequiredMixin, View):

    def get(self, request, pk):
        customer = Customer.objects.get(id=pk)
        orders = customer.order_set.all()
        order_count = orders.count()
        my_filter = OrderFilter(request.GET, queryset=orders)
        orders = my_filter.qs
        context = {'customer': customer,
                   'orders': orders,
                   'order_count': order_count,
                   'my_filter': my_filter
                   }
        return render(request, 'accounts/customer.html', context)


class CreateOrderView(LoginRequiredMixin, View):

    def get(self, request):
        form = OrderForm()
        context = {'form': form
                   }
        return render(request, 'accounts/order_form.html', context)

    def post(self, request):
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

        context = {'form': form
                   }
        return render(request, 'accounts/order_form.html', context)


class UpdateOrderView(LoginRequiredMixin, View):

    def get(self, request, pk):
        order = Order.objects.get(id=pk)
        form = OrderForm(instance=order)
        context = {'form': form}
        return render(request, 'accounts/order_form.html', context)

    def post(self, request, pk):
        order = Order.objects.get(id=pk)
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('home')

        context = {'form': form
                   }
        return render(request, 'accounts/order_form.html', context)


class DeleteOrderView(LoginRequiredMixin, View):
    def get(self, request, pk):
        order = Order.objects.get(id=pk)
        context = {'order': order
                   }
        return render(request, 'accounts/delete.html', context)

    def post(self, request, pk):
        order = Order.objects.get(id=pk)
        order.delete()
        return redirect('home')


class LoginView(View):
    def get(self, request):
        form = CreateUserForm
        context = {'form': form
                   }
        return render(request, 'accounts/login.html', context)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect')
            return redirect('login')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


class RegisterView(View):
    def get(self, request):
        form = CreateUserForm
        context = {'form': form
                   }
        return render(request, 'accounts/register.html', context)

    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('login')

        context = {'form': form
                   }
        return render(request, 'accounts/register.html', context)





