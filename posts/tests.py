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

class PostEditTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@gmail.com", password="password"
        )
        self.post = Post.objects.create(
            title="Test Post", text="This is a test post", author=self.user
        )

    def test_post_edit_with_valid_data(self):
        # Log in as the user
        self.client.login(username="testuser", password="password")

        # Prepare POST data
        post_data = {
            "title": "New Title",
            "text": "New text",
            "tags": "tag1,tag2,tag3",
            ),
        }

        # Make the POST request to edit the post
        response = self.client.post(
            reverse("post_edit", kwargs={"pk": self.post.pk}), data=post_data
        )

        # Refresh the post from the database
        self.post.refresh_from_db()

        # Check that the post was edited correctly
        self.assertEqual(self.post.title, "New Title")
        self.assertEqual(self.post.text, "New text")
        self.assertEqual(self.post.author, self.user)
        self.assertEqual(self.post.tags.count(), 3)
        self.assertTrue(self.post.tags.filter(name="tag1").exists())
        self.assertTrue(self.post.tags.filter(name="tag2").exists())
        self.assertTrue(self.post.tags.filter(name="tag3").exists())
