import datetime
from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Post, Comment

class ComentModelTests(TestCase):
    def setUp(self):
        default_user=User.objects.create(username='default')
        default_post=Post.objects.create(author=default_user, title='Post test', text='Loren ipsum')
        Comment.objects.create(post=default_post, user=default_user, text='Loren ipsum')


class PostModelTests(TestCase):
    def setUp(self):
        default_user=User.objects.create(username='default')
        Post.objects.create(author=default_user, title='Post test', text='Loren ipsum')
    
    def test_published_date(self):
        post = Post.objects.first()
        self.assertIsNone(post.published_date)
        post.publish()
        self.assertIsNotNone(post.published_date)


def create_post(text, days):
    """
    Create a post with the given `text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Post.objects.create(text=text, published_date=time, author= User.objects.first())


class ViewTests(TestCase):
    def setUp(self):
        User.objects.create(username='admin')
        
    def test_empty_list(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['posts'], [])
        
    def test_past_post(self):
        """
        Posts with a published_date in the past are displayed on the
        index page.
        """
        post = create_post(text="Past post.", days=-30)
        response = self.client.get(reverse('post_list'))
        self.assertQuerysetEqual(
            response.context['posts'],
            [post],
        )

    def test_future_post(self):
        """
        Posts with a published_date in the future are not displayed on the
        index page.
        """
        create_post(text="Future post.", days=30)
        response = self.client.get(reverse('post_list'))
        self.assertQuerysetEqual(
            response.context['posts'],
            [],
        )        
        
        
    def test_post_detail(self):
        post = create_post(text="Past post.", days=1)
        id = str(post.pk)
        response = self.client.get(reverse('post_detail',args=[id]))
        self.assertEqual(response.status_code, 200)
 