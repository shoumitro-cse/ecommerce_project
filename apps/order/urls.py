from django.urls import path
from .views import OrderListCreateView, OrderRUDAPIView


urlpatterns = [
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderRUDAPIView.as_view(), name='order-retrieve-update'),
]
