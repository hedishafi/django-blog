# accounts/tests.py

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class AccountsTests(TestCase):

    def setUp(self):
        self.client = Client()

        # Adjust URL names if different in your accounts/urls.py
        self.signup_url = reverse('accounts:signup')
        self.login_url = reverse('accounts:login')
        self.logout_url = reverse('accounts:logout')

        # Create a test user for login/logout tests
        User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='Testpass123!'
        )

    def test_signup_page_loads_correctly(self):
        """Test that the signup page returns 200"""
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)

    def test_signup_success_creates_user_and_redirects(self):
        """Test successful user registration"""
        response = self.client.post(self.signup_url, {
            'username': 'newuser',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!'
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_signup_password_mismatch(self):
        """Test signup fails when passwords don't match"""
        response = self.client.post(self.signup_url, {
            'username': 'baduser',
            'password1': 'Pass123!',
            'password2': 'Different123!'
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The two password fields didn’t match.")
        self.assertFalse(User.objects.filter(username='baduser').exists())

    def test_login_page_loads_correctly(self):
        """Test login page is accessible"""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)

    def test_login_success(self):
        """Test valid credentials allow login"""
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'Testpass123!'
        }, follow=True)

        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_invalid_credentials(self):
        """Test wrong password is rejected"""
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpassword'
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a correct username and password")
        self.assertFalse(response.context['user'].is_authenticated)

    def test_logout(self):
        """Test logout clears the session"""
        # Login first
        self.client.login(username='testuser', password='Testpass123!')
        
        response = self.client.get(self.logout_url, follow=True)

        self.assertFalse(response.context['user'].is_authenticated)