from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Article
from . import forms

class ArticleViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='author', password='Testpass123!')
        self.article = Article.objects.create(
            title='Test Article',
            slug='test-article',
            body='This is a test article body.',
            author=self.user
        )

    def test_article_list_view(self):
        response = self.client.get(reverse('articles:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.article.title)

    def test_article_detail_view(self):
        response = self.client.get(reverse('articles:detail', args=[self.article.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['article'], self.article)

    def test_article_create_view_requires_login(self):
        response = self.client.get(reverse('articles:create'))
        self.assertRedirects(response, '/accounts/login/?next=/articles/create/')

    def test_article_create_view(self):
        self.client.login(username='author', password='Testpass123!')
        response = self.client.post(reverse('articles:create'), {
            'title': 'New Article',
            'slug': 'new-article',
            'body': 'This is the body of the new article.'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertTrue(Article.objects.filter(title='New Article').exists())

    def test_article_create_view_invalid_data(self):
        self.client.login(username='author', password='Testpass123!')
        response = self.client.post(reverse('articles:create'), {
            'title': '',
            'slug': '',
            'body': ''
        })
        self.assertEqual(response.status_code, 200)  # Form returns errors
        self.assertFalse(Article.objects.filter(title='').exists())
