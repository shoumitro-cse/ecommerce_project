from django.contrib.auth import get_user_model
from apps.base.tests import APITestCase


class UserModelTests(APITestCase):

    def test_user_creation(self):
        self.assertEqual(get_user_model().objects.count(), 1)
