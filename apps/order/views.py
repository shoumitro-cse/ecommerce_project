from functools import cached_property

from django.db import transaction
from rest_framework import generics
from rest_framework.generics import get_object_or_404

from .constant import SHIPPED, DELIVERED
from .models import Order
from .serializers import OrderSerializer
from apps.base.mixins.exception import OrderExceptionMixin, OrderException
from apps.order.mixins.order_mixin import OrderManagerMixin


class OrderListCreateView(OrderManagerMixin, OrderExceptionMixin, generics.ListCreateAPIView):
    """
    API endpoint for listing and creating orders.

    This endpoint allows users to list their existing orders or create a new order.

    Responses:
     - GET request: Retrieve a list of existing orders for the authenticated user.
     - POST request: Create a new order with the provided data.

    Examples:
     - To list orders:
        ```http
        GET /orders/
        ```

     - To create a new order:
        ```http
        POST /orders/
        ```
        Payload:
        ```json
        {
            "order_items": [
                {"product": 1, "quantity": 2},
                {"product": 2, "quantity": 1}
            ]
            // Additional fields for the order
        }
        ```
    """

    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related(
            "order_items", "order_items__product").select_related("user").order_by("-id")

    @transaction.atomic
    def perform_create(self, serializer):
        self._process_order(serializer)  # add order


class OrderRUDAPIView(OrderManagerMixin, OrderExceptionMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting a specific order.

    This endpoint allows users to retrieve details, update, or delete a specific order.

    Responses:
     - GET request: Retrieve details for a specific order.
     - PUT/PATCH request: Update a specific order.
     - DELETE request: Delete a specific order.

    Examples:
     - To retrieve details for a specific order:
        ```http
        GET /orders/{order_id}/
        ```

     - To update a specific order:
        ```http
        PUT /orders/{order_id}/
        ```
        Payload:
        ```json
        {
            "order_items": [
                {"product": 1, "quantity": 3},
                {"product": 2, "quantity": 2}
            ]
            // Additional fields for the order update
        }
        ```

     - To delete a specific order:
        ```http
        DELETE /orders/{order_id}/
        ```
    """

    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(
            pk=self.kwargs[self.lookup_field], user=self.request.user
        ).prefetch_related("order_items", "order_items__product").select_related("user")

    @cached_property
    def order(self):
        return super().get_object()

    def get_object(self):
        return self.order

    @transaction.atomic
    def perform_update(self, serializer):
        # Check if the order is in a modifiable status
        if self.order.order_status not in [SHIPPED, DELIVERED]:
            if serializer.validated_data.get("order_items", None) is not None:
                # Delete existing order items and create new ones
                self.restore_order_items(self.order)  # restore order
                self._process_order(serializer)  # add order
        else:
            # If the order status is not eligible for modification, raise an exception
            raise OrderException("Order status not eligible for modification")
