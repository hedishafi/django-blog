from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class AccountTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Runs once, CI-friendly
        cls.user = User.objects.create_user(username='testuser', password='testpass')

    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('accounts:signup')
        self.login_url = reverse('accounts:login')
        self.logout_url = reverse('accounts:logout')

    # ---------------- URL Tests ----------------
    def test_urls_exist(self):
        for url in [self.signup_url, self.login_url]:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

        response = self.client.get(self.logout_url)
        self.assertIn(response.status_code, [302, 200])

    # ---------------- Signup Tests ----------------
    def test_signup_valid(self):
        response = self.client.post(self.signup_url, {
            'username': 'newuser',
            'password1': 'newpass123',
            'password2': 'newpass123'
        }, follow=True)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertEqual(response.status_code, 200)

    def test_signup_password_mismatch(self):
        response = self.client.post(self.signup_url, {
            'username': 'baduser',
            'password1': 'pass123',
            'password2': 'pass456'
        }, follow=True)
        self.assertContains(response, "password fields")
        self.assertFalse(User.objects.filter(username='baduser').exists())

    def test_signup_missing_username(self):
        response = self.client.post(self.signup_url, {
            'username': '',
            'password1': 'pass123',
            'password2': 'pass123'
        }, follow=True)
        self.assertContains(response, "This field is required")

    # ---------------- Login Tests ----------------
    def test_login_valid(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpass'
        }, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertEqual(response.status_code, 200)

    def test_login_invalid_password(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpass'
        }, follow=True)
        self.assertContains(response, "correct username and password")
        self.assertFalse(response.context['user'].is_authenticated)

    def test_login_nonexistent_user(self):
        response = self.client.post(self.login_url, {
            'username': 'nouser',
            'password': 'pass123'
        }, follow=True)
        self.assertContains(response, "correct username and password")

    # ---------------- Logout Tests ----------------
    def test_logout_authenticated_user(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(self.logout_url, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_logout_anonymous_user(self):
        response = self.client.post(self.logout_url, follow=True)
        # just ensure it doesn't crash and redirects
        self.assertIn(response.status_code, [200, 302])
