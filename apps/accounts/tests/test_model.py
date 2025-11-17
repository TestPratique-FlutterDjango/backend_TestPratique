from django.test import TestCase
from apps.accounts.models import User


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            account_type=User.AccountType.PRIVATE
        )
    
    def test_user_creation(self):
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('testpass123'))
        self.assertEqual(self.user.full_name, 'Test User')
    
    def test_user_is_not_professional(self):
        self.assertFalse(self.user.is_professional())