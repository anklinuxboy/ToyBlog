from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Post

class BlogTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username = 'testuser',
            email = 'test@gmail.com',
            password = 'password'
        )

        self.post = Post.objects.create(
            title = 'title',
            author = self.user,
            body = 'body'
        )

    def test_str_rep(self):
        self.assertEqual(str(self.post), self.post.title)

    def test_content(self):
        self.assertEqual(f'{self.post.title}', 'title')
        self.assertEqual(f'{self.post.author}', 'testuser')
        self.assertEqual(f'{self.post.body}', 'body')

    def test_post_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'body')
        self.assertTemplateUsed(response, 'home.html')

    def test_post_detail_view(self):
        response = self.client.get('/post/1')
        no_response = self.client.get('/post/100000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'title')
        self.assertTemplateUsed(response, 'post_detail.html')
