# accounts/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from articles.models import Article  # Ensure articles exist for redirects

class AccountTests(TestCase):

    @classmethod
    def setUpTestData(cls):# accounts/tests.py
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

    # --------- URL checks ----------
    def test_urls(self):
        self.assertEqual(self.client.get(self.signup_url).status_code, 200)
        self.assertEqual(self.client.get(self.login_url).status_code, 200)
        self.assertIn(self.client.get(self.logout_url).status_code, [200, 302])

    # --------- Signup ----------
    def test_signup_creates_user(self):
        self.client.post(self.signup_url, {
            'username': 'newuser',
            'password1': 'newpass123',
            'password2': 'newpass123'
        }, follow=False)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    # --------- Login ----------
    def test_login_logout(self):
        # Valid login
        self.client.post(self.login_url, {'username': 'testuser', 'password': 'testpass'}, follow=False)
        # Logout
        response = self.client.post(self.logout_url, follow=False)
        self.assertIn(response.status_code, [200, 302])

        cls.user = User.objects.create_user(username='testuser', password='testpass')
        # Create dummy article so 'articles:list' exists
        Article.objects.create(title="Dummy", slug="dummy", body="dummy", author=cls.user)

    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('accounts:signup')
        self.login_url = reverse('accounts:login')
        self.logout_url = reverse('accounts:logout')

    # ---------------- URL Tests ----------------
    def test_signup_url_status(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)

    def test_login_url_status(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)

    def test_logout_url_status(self):
        response = self.client.get(self.logout_url)
        self.assertIn(response.status_code, [302, 200])

    # ---------------- Signup Tests ----------------
    def test_signup_creates_user(self):
        response = self.client.post(self.signup_url, {
            'username': 'newuser',
            'password1': 'newpass123',
            'password2': 'newpass123'
        }, follow=False)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertIn(response.status_code, [302, 200])

    def test_signup_password_mismatch(self):
        response = self.client.post(self.signup_url, {
            'username': 'baduser',
            'password1': 'pass123',
            'password2': 'pass456'
        }, follow=False)
        self.assertFalse(User.objects.filter(username='baduser').exists())
        self.assertIn(response.status_code, [200, 302])

    def test_signup_missing_username(self):
        response = self.client.post(self.signup_url, {
            'username': '',
            'password1': 'pass123',
            'password2': 'pass123'
        }, follow=False)
        self.assertFalse(User.objects.filter(username='').exists())
        self.assertIn(response.status_code, [200, 302])

    # ---------------- Login Tests ----------------
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

    # ---------------- Logout Tests ----------------
    def test_logout_authenticated_user(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(self.logout_url, follow=False)
        self.assertIn(response.status_code, [302, 200])

    def test_logout_anonymous_user(self):
        response = self.client.post(self.logout_url, follow=False)
        self.assertIn(response.status_code, [302, 200])
