from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

class AccountsViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user_data = {
            'username': 'testuser',
            'password1': 'Testpass123!',
            'password2': 'Testpass123!'
        }

    def test_signup_view(self):
    response = self.client.post(reverse('accounts:signup'), self.user_data)
    self.assertEqual(response.status_code, 302)  # redirect after signup
    self.assertTrue(User.objects.filter(username='testuser').exists())
    def test_login_view(self):
        User.objects.create_user(username='loginuser', password='Testpass123!')
        login_data = {'username': 'loginuser', 'password': 'Testpass123!'}
        response = self.client.post(reverse('accounts:login'), login_data)
        self.assertEqual(response.status_code, 302)  # redirect after login

    def test_logout_view(self):
        user = User.objects.create_user(username='logoutuser', password='Testpass123!')
        self.client.login(username='logoutuser', password='Testpass123!')
        response = self.client.post(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)  # redirect after logout
