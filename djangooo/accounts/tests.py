# accounts/tests.py
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

    # -------- URL checks --------
    def test_urls(self):
        self.assertEqual(self.client.get(self.signup_url).status_code, 200)
        self.assertEqual(self.client.get(self.login_url).status_code, 200)
        self.assertIn(self.client.get(self.logout_url).status_code, [200, 302])

    # -------- Signup test --------
    def test_signup_creates_user(self):
        self.client.post(self.signup_url, {
            'username': 'newuser',
            'password1': 'newpass123',
            'password2': 'newpass123'
        }, follow=False)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    # -------- Login + Logout test --------
    def test_login_logout(self):
        self.client.post(self.login_url, {'username': 'testuser', 'password': 'testpass'}, follow=False)
        response = self.client.post(self.logout_url, follow=False)
        self.assertIn(response.status_code, [200, 302])
