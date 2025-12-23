from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Article
from django.urls import reverse
from unittest.mock import patch
from django.conf import settings

class ArticleModelTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='author', password='Testpass123!')

    def test_article_creation(self):
        article = Article.objects.create(
            title='Test Article',
            slug='test-article',
            body='This is the body of the test article.',
            author=self.user
        )
        self.assertEqual(str(article), 'Test Article')
        self.assertEqual(article.snippet(), 'This is the body of the test article....')

class ArticleViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='author', password='Testpass123!')
        self.article = Article.objects.create(
            title='Test Article',
            slug='test-article',
            body='This is the body of the test article.',
            author=self.user
        )

    @patch('django.template.loader.get_template')
    def test_article_detail_view(self, mock_get_template):
        # Mock the template to return a dummy response
        mock_get_template.return_value.render.return_value = "<html></html>"
        response = self.client.get(reverse('articles:detail', args=[self.article.slug]))
        self.assertEqual(response.status_code, 200)

    def test_article_list_view(self):
        response = self.client.get(reverse('articles:list'))
        self.assertEqual(response.status_code, 200)

    def test_article_create_view_requires_login(self):
        response = self.client.get(reverse('articles:create'))
        self.assertEqual(response.status_code, 302)  # redirect to login

    def test_template_dirs(self):
        # Print the template directories being searched
        templates = settings.TEMPLATES[0]['DIRS']
        print("Template directories:", templates)
        self.assertTrue(templates)  # Ensure directories are listed