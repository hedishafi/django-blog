from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from articles.models import Article
from articles.forms import CreateArticle

class ArticleTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # URLs
        self.article_list_url = reverse('articles:list')
        self.article_create_url = reverse('articles:create')

        # Sample article
        self.article = Article.objects.create(
            title="Test Article",
            slug="test-article",
            body="This is a test article.",
            author=self.user
        )

    # ---------------- Model Tests ----------------
    def test_article_creation(self):
        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(str(self.article), "Test Article")
        self.assertEqual(self.article.snippet(), "This is a test article....")
        self.assertEqual(self.article.author.username, 'testuser')

    # ---------------- URL Tests ----------------
    def test_article_list_url_exists(self):
        response = self.client.get(self.article_list_url)
        self.assertEqual(response.status_code, 200)

    def test_article_detail_url_exists(self):
        url = reverse('articles:detail', args=[self.article.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_article_create_url_redirect_if_not_logged_in(self):
        response = self.client.get(self.article_create_url)
        self.assertEqual(response.status_code, 302)  # should redirect to login

    # ---------------- View Tests ----------------
    def test_article_list_view(self):
        response = self.client.get(self.article_list_url)
        self.assertContains(response, self.article.title)
        self.assertEqual(response.status_code, 200)

    def test_article_detail_view(self):
        url = reverse('articles:detail', args=[self.article.slug])
        response = self.client.get(url)
        self.assertContains(response, self.article.body)
        self.assertEqual(response.status_code, 200)

    def test_article_create_view_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(self.article_create_url, {
            'title': 'Another Article',
            'slug': 'another-article',
            'body': 'Some body text',
            'thumb': ''
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Article.objects.filter(slug='another-article').exists())

    # ---------------- Form Tests ----------------
    def test_article_form_valid(self):
        form_data = {'title': 'Form Article', 'slug': 'form-article', 'body': 'Body text'}
        form = CreateArticle(data=form_data)
        self.assertTrue(form.is_valid())

    def test_article_form_invalid(self):
        form_data = {'title': '', 'slug': '', 'body': ''}
        form = CreateArticle(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        self.assertIn('slug', form.errors)
