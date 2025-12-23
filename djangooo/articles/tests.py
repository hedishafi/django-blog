from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Article
from django.urls import reverse

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

    def test_article_list_view(self):
        response = self.client.get(reverse('articles:list'))
        self.assertEqual(response.status_code, 200)

    def test_article_detail_view(self):
        response = self.client.get(reverse('articles:detail', args=[self.article.slug]))
        self.assertEqual(response.status_code, 200)

    def test_article_create_view_requires_login(self):
        response = self.client.get(reverse('articles:create'))
        self.assertEqual(response.status_code, 302)  # redirect to login
