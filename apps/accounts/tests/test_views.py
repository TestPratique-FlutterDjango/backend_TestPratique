from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.accounts.models import User


class RegisterViewTest(APITestCase):
    def test_register_private_account(self):
        url = reverse('accounts:register')
        data = {
            'email': 'newuser@example.com',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!',
            'first_name': 'New',
            'last_name': 'User',
            'address': '123 Test St',
            'account_type': 'PRIVATE'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('tokens', response.data)
        self.assertEqual(User.objects.count(), 1)