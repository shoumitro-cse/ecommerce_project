from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from apps.order.models import Order
from apps.product.models import Product, ProductReview


class APITestCase(TestCase):
    """
     python manage.py test apps.base
    """

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.product = Product.objects.create(
            name='Test Product',
            description='Product description',
            price=29.99,
            stock_quantity=100,
            created_by=self.user,
            updated_by=self.user
        )
        self.order = Order.objects.create(
            user=self.user,
            total_price=29.99,
            order_status='pending',
            created_by=self.user,
            updated_by=self.user
        )
        self.review = ProductReview.objects.create(
            user=self.user,
            product=self.product,
            text='Great product!',
            rating=5,
            created_by=self.user,
            updated_by=self.user
        )
        self.token = self.get_access_token()

    def get_access_token(self):
        refresh = RefreshToken.for_user(self.user)
        return str(refresh.access_token)

    def set_auth_header(self, request):
        request.headers['Authorization'] = f'Bearer {self.token}'

