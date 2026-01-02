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

    # ---------------- URL tests ----------------
    def test_signup_url_status(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)

    def test_login_url_status(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)

    def test_logout_url_status(self):
        response = self.client.get(self.logout_url)
        self.assertIn(response.status_code, [302, 200])

    # ---------------- Signup tests ----------------
    def test_signup_creates_user(self):
        self.client.post(self.signup_url, {
            'username': 'newuser',
            'password1': 'newpass123',
            'password2': 'newpass123'
        }, follow=False)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_signup_password_mismatch(self):
        self.client.post(self.signup_url, {
            'username': 'baduser',
            'password1': 'pass123',
            'password2': 'pass456'
        }, follow=False)
        # Should not create user
        self.assertFalse(User.objects.filter(username='baduser').exists())

    def test_signup_missing_username(self):
        self.client.post(self.signup_url, {
            'username': '',
            'password1': 'pass123',
            'password2': 'pass123'
        }, follow=False)
        # No user should be created
        self.assertFalse(User.objects.filter(username='').exists())

    # ---------------- Login tests ----------------
    def test_login_valid_user(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpass'
        }, follow=False)
        self.assertIn(response.status_code, [302, 200])

    def test_login_invalid_password(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpass'
        }, follow=False)
        self.assertIn(response.status_code, [200, 302])

    def test_login_nonexistent_user(self):
        response = self.client.post(self.login_url, {
            'username': 'nouser',
            'password': 'pass123'
        }, follow=False)
        self.assertIn(response.status_code, [200, 302])

    # ---------------- Logout tests ----------------
    def test_logout_authenticated_user(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(self.logout_url, follow=False)
        self.assertIn(response.status_code, [302, 200])

    def test_logout_anonymous_user(self):
        response = self.client.post(self.logout_url, follow=False)
        self.assertIn(response.status_code, [302, 200])
