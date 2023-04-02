from django.test import Client, TestCase
from django.urls import reverse

from users.models import User

from .models import Post


class PostEditTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", email="test@gmail.com", password="password")
        self.post = Post.objects.create(title="Test Post", text="This is a test post", author=self.user)

    def test_post_edit_with_valid_data(self):
        # Log in as the user
        self.client.login(username="testuser", password="password")

        # Prepare POST data
        post_data = {
            "title": "New Title",
            "text": "New text",
            "tags": "tag1,tag2,tag3",
        }

        # Make the POST request to edit the post
        self.client.post(reverse("post_edit", kwargs={"pk": self.post.pk}), data=post_data)

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
