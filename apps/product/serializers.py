from rest_framework import serializers
from .models import Product, ProductReview
from ..user.serializers import UserSerializer


class ProductSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "price", "stock_quantity", "created_by"]


class ProductReviewSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = ProductReview
        fields = ['id', 'user', 'product', 'text', 'rating']
        extra_kwargs = {"product": {"read_only": True}, "user": {"read_only": True}}
