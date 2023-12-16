from apps.base.tests import APITestCase
from apps.order.models import Order
import json
from rest_framework import status


class OrderModelTests(APITestCase):

    def test_order_creation(self):
        self.assertEqual(Order.objects.count(), 1)


class OrderAPITests(APITestCase):

    def test_order_list(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get('/api/orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_order(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        data = {
            "order_items": [
                {"product": self.product.id, "quantity": 2}
            ],
            "order_status": "pending"
        }
        response = self.client.post('/api/orders/', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_order(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(f'/api/orders/{self.order.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
