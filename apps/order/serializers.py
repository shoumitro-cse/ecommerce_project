from rest_framework import serializers
from .models import Order, OrderItem
from apps.product.serializers import ProductSerializer
from apps.user.serializers import UserSerializer


class OrderItemReadSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    total_price = serializers.DecimalField(required=True, max_digits=10, decimal_places=2)

    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "total_price"]


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ["product", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Order
        exclude = ["updated_by", "created_by", "created_at", "updated_at"]
        extra_kwargs = {
            "total_price": {"read_only": True}
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        order_items_queryset = instance.order_items.all()
        if self.context["request"].method in ["PUT", "PATCH"]:
            order_items_queryset = order_items_queryset.select_related("product")
        data["order_items"] = OrderItemReadSerializer(instance=order_items_queryset, many=True).data
        return data

