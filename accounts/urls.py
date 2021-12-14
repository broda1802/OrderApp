from django.urls import path
from .views import HomeView, ProductView, CustomerView, CreateOrderView, UpdateOrderView, DeleteOrderView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('products/', ProductView.as_view(), name='products'),
    path('customer/<int:pk>/', CustomerView.as_view(), name='customer'),
    path('create_order/', CreateOrderView.as_view(), name='crate_order'),
    path('update_order/<int:pk>/', UpdateOrderView.as_view(), name='update_order'),
    path('delete_order/<int:pk>/', DeleteOrderView.as_view(), name='delete_order'),
]
