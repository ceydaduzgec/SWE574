from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from posts.models import Post
from spaces.models import Space

User = get_user_model()


class SpaceViewsTestCase(TestCase):
    def setUp(self):
        # create a test user
        self.user = User.objects.create_user(username="testuser", email="testuser@gmail.com", password="password")

        # create a test space
        self.space = Space.objects.create(
            name="Test Space",
            description="This is a test space.",
            owner=self.user,
        )

    def test_join_space_view(self):
        # log in as the test user
        self.client.login(username="testuser", password="password")

        # make a GET request to the join space view
        response = self.client.get(reverse("join_space", args=[self.space.pk]))

        # check that the response is a redirect
        self.assertEqual(response.status_code, 302)

        # check that the user is now a member of the space
        self.assertIn(self.user, self.space.members.all())

    def test_my_spaces_list_authenticated(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("my_spaces_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "my_spaces_list.html")
        self.assertIn(self.space, response.context["spaces"])

    def test_space_detail_view(self):
        user = User.objects.create_user(username="testuser2", email="testuser2@gmail.com", password="password")
        # create a space
        space = Space.objects.create(name="Test Space", description="Test description", owner=user)
        # create a post
        post = Post.objects.create(title="Test Post", text="Test content", author=user)
        post.spaces.add(space)

        # make a GET request to the space detail view
        response = self.client.get(reverse("space_detail", args=[space.pk]))

        # assert that the response is successful
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context["space"], space)

        self.assertIn(post, response.context["posts"])
        self.assertTemplateUsed(response, "space_detail.html")
