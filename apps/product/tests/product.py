from apps.base.tests import APITestCase
from apps.product.models import Product
from rest_framework import status


class ProductModelTests(APITestCase):

    def test_product_creation(self):
        self.assertEqual(Product.objects.count(), 1)


class ProductAPITests(APITestCase):

    def test_product_list(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_product(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        data = {
            "name": "New Product",
            "description": "Product description",
            "price": 29.99,
            "stock_quantity": 100
        }
        response = self.client.post('/api/products/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_product(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(f'/api/products/{self.product.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
