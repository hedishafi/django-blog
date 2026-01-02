from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class AccountTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('accounts:signup')
        self.login_url = reverse('accounts:login')
        self.logout_url = reverse('accounts:logout')

        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')

    # ---------------- Model Tests ----------------
    def test_user_creation(self):
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(self.user.username, 'testuser')

    # ---------------- URL Tests ----------------
    def test_signup_url_exists(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)

    def test_login_url_exists(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)

    def test_logout_url_redirects(self):
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)

    # ---------------- Signup View Tests ----------------
    def test_signup_valid(self):
        response = self.client.post(self.signup_url, {
            'username': 'newuser',
            'password1': 'newpass123',
            'password2': 'newpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_signup_password_mismatch(self):
        response = self.client.post(self.signup_url, {
            'username': 'baduser',
            'password1': 'pass123',
            'password2': 'pass456'
        })
        self.assertEqual(response.status_code, 200)
        # CI-safe check: look for part of the message instead of exact match
        self.assertContains(response, "password fields")
        self.assertFalse(User.objects.filter(username='baduser').exists())

    def test_signup_missing_username(self):
        response = self.client.post(self.signup_url, {
            'username': '',
            'password1': 'pass123',
            'password2': 'pass123'
        })
        self.assertEqual(response.status_code, 200)
        # CI-safe check: look for part of the message instead of exact match
        self.assertContains(response, "This field is required")

    # ---------------- Login View Tests ----------------
    def test_login_valid(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_invalid_password(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "correct username and password")
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_login_nonexistent_user(self):
        response = self.client.post(self.login_url, {
            'username': 'nouser',
            'password': 'pass123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "correct username and password")

    # ---------------- Logout View Tests ----------------
    def test_logout_authenticated_user(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)

    def test_logout_anonymous_user(self):
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)
