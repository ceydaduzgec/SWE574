from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Post
from users.models import Badge, User


class PostEditTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", email="test@gmail.com", password="password")

        # Create the badge
        self.badge = Badge.objects.create(name="Post Duck", description="Awarded for creating a post")

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

    def test_invalid_data(self):
        post_data = {
            "title": "New Title",
            "tags": "tag1,tag2,tag3",
        }
        self.client.post(reverse("post_edit", kwargs={"pk": self.post.pk}), data=post_data)


# from django.contrib.auth import authenticate, get_user_model
# from django.db.models import Q
# from django.test import TestCase

# from users.factory import UserFactory

# from .models import Post

# User = get_user_model()


# class PostTestCase(TestCase):
#     def setUp(cls):
#         cls.user = UserFactory(username="eralp", email="abc@abc.com", password="1234")

#         Post.objects.create(
#             author=cls.user,
#             title="Test the Test",
#             text="Testing the Test Works",
#             upload="a",
#         )

#     def test_post_exists(self):
#         p = Post.objects.all()
#         self.assertTrue(p.exists())

#     def test_user_exists(self):
#         user = User.objects.get(username="eralp")
#         self.assertTrue(user)

# def test_user_login(self):
#     user = authenticate(username="eralp", password="1234")
#     self.assertTrue(user)

# def test_user_register(self):
#     data = {
#         "username": "testuser",
#         "email": "abc@gmail.com",
#         "password1": "Eralp123!",
#         "password2": "Eralp123!",
#     }
#     form = UserCreationForm(data)
#     self.assertTrue(form.is_valid())

# def test_user_cannot_register_with_common_password(self):
#     data = {
#         "username": "testuser",
#         "email": "abc@gmail.com",
#         "password1": "test123",
#         "password2": "test123",
#     }
#     form = UserCreationForm(data)
#     self.assertFalse(form.is_valid())
#     self.assertIn("This password is too common.", form.errors.as_text())
#     self.assertIn("This password is too short.", form.errors.as_text())

# def test_is_password_username_valid(self):
#     user = authenticate(username="sevval", password="1234")
#     self.assertFalse(user)

# def test_search(self):
#     user = User.objects.get(username="eralp")

#     post1 = Post.objects.create(
#         author=user,
#         title="Test Post 1",
#         text="This is the first test post",
#         upload="x",
#     )
#     post2 = Post.objects.create(
#         author=user,
#         title="Test Post 2",
#         text="This is the second test post",
#         upload="y",
#     )

#     searched = "Test Post 1"
#     posts_s_ = Post.objects.filter(Q(title__icontains=searched) | Q(text__icontains=searched))
#     self.assertTrue(posts_s_.exists())
#     self.assertEqual(posts_s_.count(), 1)
#     self.assertEqual(posts_s_.first(), post1)

#     searched = "Test Post 2"
#     posts_s_ = Post.objects.filter(Q(title__icontains=searched) | Q(text__icontains=searched))
#     self.assertTrue(posts_s_.exists())
#     self.assertEqual(posts_s_.count(), 1)
#     self.assertEqual(posts_s_.first(), post2)

#     searched = "test"
#     posts = Post.objects.filter(Q(title__icontains=searched) | Q(text__icontains=searched))
#     self.assertTrue(posts.exists())
#     self.assertEqual(posts.count(), 3)

#     searched = "eralp"
#     posts = Post.objects.filter(Q(title__icontains=searched) | Q(text__icontains=searched))
#     self.assertFalse(posts.exists())
#     self.assertEqual(posts.count(), 0)


# class TagTestCase(TestCase):
#     def setUp(self):
#         Tag.objects.create(nauser="django")
#         Tag.objects.create(nauser="Test Tag")

#     def test_tags_have_nausers(self):
#         django_tag = Tag.objects.get(nauser="django")
#         test_tag = Tag.objects.get(nauser="Test Tag")
#         self.assertEqual(django_tag.nauser, "django")
#         self.assertFalse(test_tag.nauser, "da_jango")


# class CommentTestCase(TestCase):
#     def setUp(self):
#         user = UserFactory()
#         Comment.objects.create(author=user, text="Django is Nice")

#     def test_comment_has_author(self):
#         comment = Comment.objects.get(text="Django is Nice")
#         self.assertEqual(comment.author.username, "user_A")

#     def test_comment_has_text(self):
#         comment = Comment.objects.get(text="Django is Nice")
#         self.assertEqual(comment.text, "Django is Nice")


# class BookmarkViewTest(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = UserFactory()
#         self.post = Post.objects.create(title="Test Post", content="Test content", author=self.user)

#     def test_add_bookmark_view(self):
#         self.client.force_login(self.user)
#         url = reverse("add_bookmark", args=[self.post.id])
#         response = self.client.post(url)
#         self.assertEqual(response.status_code, 302)
#         self.assertTrue(self.user.bookmarks.filter(pk=self.post.id).exists())

#     def test_remove_bookmark_view(self):
#         self.client.force_login(self.user)
#         self.user.bookmarks.add(self.post)
#         url = reverse("remove_bookmark", args=[self.post.id])
#         response = self.client.post(url)
#         self.assertEqual(response.status_code, 302)
#         self.assertFalse(self.user.bookmarks.filter(pk=self.post.id).exists())


# class BadgeTestCase(TestCase):
#     def setUp(self):
#
#
#         self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpassword")
#         post = Post.objects.create(title="Test Post", text="This is a test post", author=self.user)
#         Comment.objects.create(author=self.user, text="Test comment", post=post)
#         self.comment_badge = Badge.objects.create(
#             name="Commenter",
#             description="Earned by users who have posted 10 or more comments.",
#
#         )
#
#     def test_comment_badge_award(self):
#         # Create 9 comments, user should not earn the badge yet
#         for _ in range(9):
#             Comment.objects.create(author=self.user, text="Test comment")
#
#         self.assertFalse(UserBadge.objects.filter(user=self.user, badge=self.comment_badge).exists())
#
#         # Create the 10th comment, user should now earn the badge
#         Comment.objects.create(author=self.user, text="Test comment")
#
#         self.assertTrue(UserBadge.objects.filter(user=self.user, badge=self.comment_badge).exists())
#
#     # Test when a user deletes comments. The badge should be revoked if the user no longer meets the requirement.
#     def test_comment_badge_revoke(self):
#         # Create 10 comments, user should earn the badge
#         for _ in range(10):
#             Comment.objects.create(author=self.user, text="Test comment")
#
#
#         self.assertTrue(UserBadge.objects.filter(user=self.user, badge=self.comment_badge).exists())
#
#         # Delete 10 comments, user should no longer have the badge
#         for _ in range(10):
#             Comment.objects.filter(author=self.user).first().delete()
#
#         self.assertFalse(UserBadge.objects.filter(user=self.user, badge=self.comment_badge).exists())
#
#     def tearDown(self):
#         self.user.delete()
#         self.comment_badge.delete()
