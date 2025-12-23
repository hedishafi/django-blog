from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class AccountViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('accounts:signup')
        self.login_url = reverse('accounts:login')
        self.logout_url = reverse('accounts:logout')

    def test_signup_view(self):
    response = self.client.post(self.signup_url, {
        'username': 'testuser',
        'password1': 'Testpass123!',
        'password2': 'Testpass123!'
    })
    self.assertEqual(response.status_code, 200)  #  Wrong, should be 302 → will fail
    self.assertTrue(User.objects.filter(username='nonexistentuser').exists())  #  Will fail

    def test_login_view(self):
        # Create user first
        User.objects.create_user(username='testuser', password='Testpass123!')
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'Testpass123!'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after login

    def test_logout_view(self):
        # Create user first
        User.objects.create_user(username='testuser', password='Testpass123!')
        self.client.login(username='testuser', password='Testpass123!')
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)  # Redirect after logout
        self.assertFalse('_auth_user_id' in self.client.session)  # User logged out
