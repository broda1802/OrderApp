from django.shortcuts import render, redirect
from .forms import OrderForm
from .filters import OrderFilter

# Create your views here.
from django.views import View

from accounts.models import Product, Order, Customer


class HomeView(View):

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


class ProductView(View):

    def get(self, request):
        products = Product.objects.all()
        return render(request, 'accounts/products.html', {'products': products})


class CustomerView(View):

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


class CreateOrderView(View):

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


class UpdateOrderView(View):

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


class DeleteOrderView(View):
    def get(self, request, pk):
        order = Order.objects.get(id=pk)
        context = {'order': order
                   }
        return render(request, 'accounts/delete.html', context)

    def post(self, request, pk):
        order = Order.objects.get(id=pk)
        order.delete()
        return redirect('home')





