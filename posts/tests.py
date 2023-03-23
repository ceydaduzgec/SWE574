from django.contrib.auth import authenticate, get_user_model
from django.db.models import Q
from django.test import TestCase

from users.factory import UserFactory

from .models import Post

User = get_user_model()


class PostTestCase(TestCase):
    def setUp(cls):
        cls.user = UserFactory(username="eralp", email="abc@abc.com", password="1234")

        Post.objects.create(
            author=cls.user,
            title="Test the Test",
            text="Testing the Test Works",
            upload="a",
        )

    def test_post_exists(self):
        p = Post.objects.all()
        self.assertTrue(p.exists())

    def test_user_exists(self):
        user = User.objects.get(username="eralp")
        self.assertTrue(user)

    def test_is_password_username_valid(self):
        user = authenticate(username="sevval", password="1234")
        self.assertFalse(user)

    def test_search(self):
        user = User.objects.get(username="eralp")

        post1 = Post.objects.create(
            author=user,
            title="Test Post 1",
            text="This is the first test post",
            upload="x",
        )
        post2 = Post.objects.create(
            author=user,
            title="Test Post 2",
            text="This is the second test post",
            upload="y",
        )

        searched = "Test Post 1"
        posts_s_ = Post.objects.filter(Q(title__icontains=searched) | Q(text__icontains=searched))
        self.assertTrue(posts_s_.exists())
        self.assertEqual(posts_s_.count(), 1)
        self.assertEqual(posts_s_.first(), post1)

        searched = "Test Post 2"
        posts_s_ = Post.objects.filter(Q(title__icontains=searched) | Q(text__icontains=searched))
        self.assertTrue(posts_s_.exists())
        self.assertEqual(posts_s_.count(), 1)
        self.assertEqual(posts_s_.first(), post2)

        searched = "test"
        posts = Post.objects.filter(Q(title__icontains=searched) | Q(text__icontains=searched))
        self.assertTrue(posts.exists())
        self.assertEqual(posts.count(), 3)

        searched = "eralp"
        posts = Post.objects.filter(Q(title__icontains=searched) | Q(text__icontains=searched))
        self.assertFalse(posts.exists())
        self.assertEqual(posts.count(), 0)
