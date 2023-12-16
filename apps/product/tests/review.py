from apps.base.tests import APITestCase
from apps.product.models import ProductReview
import json
from rest_framework import status


class ReviewModelTests(APITestCase):

    def test_review_creation(self):
        self.assertEqual(ProductReview.objects.count(), 1)


class ReviewAPITests(APITestCase):

    def test_review_list(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(f'/api/products/{self.product.id}/reviews/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_review(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        data = {
            "text": "Great product!",
            "rating": 5
        }
        response = self.client.post(f'/api/products/{self.product.id}/reviews/', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_review(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(f'/api/products/{self.product.id}/reviews/{self.review.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
