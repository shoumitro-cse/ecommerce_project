# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import ProductAPIViewSet, ProductReviewAPIViewSet

router = DefaultRouter()
router.register(r'products', ProductAPIViewSet, basename='product')

# Nested router for product reviews
product_router = SimpleRouter()
product_router.register(r'reviews', ProductReviewAPIViewSet, basename='product-review')

urlpatterns = [
    path('', include(router.urls)),
    path('products/<int:product_id>/', include(product_router.urls)),
]
