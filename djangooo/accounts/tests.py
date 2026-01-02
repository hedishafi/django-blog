from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class AccountTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='testpass')

    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('accounts:signup')
        self.login_url = reverse('accounts:login')
        self.logout_url = reverse('accounts:logout')

    def test_signup_creates_user(self):
        self.client.post(self.signup_url, {
            'username': 'newuser',
            'password1': 'newpass123',
            'password2': 'newpass123'
        })
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_logout(self):
        # Login
        self.client.post(self.login_url, {'username': 'testuser', 'password': 'testpass'})
        # Logout via GET (safe now)
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)  # always redirect
