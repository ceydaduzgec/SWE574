from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from posts.models import Post
from spaces.models import Space
from users.models import Badge

User = get_user_model()


class SpaceViewsTestCase(TestCase):
    def setUp(self):
        # create a test user
        self.user = User.objects.create_user(username="testuser", email="testuser@gmail.com", password="password")
        # create a test badge
        self.explorer_badge = Badge.objects.create(name="Explorer", description="You explored a new space!")
        # create a test post
        self.post_duck_badge = Badge.objects.create(name="Post Duck", description="Some description")
        # create a test space
        self.space = Space.objects.create(
            name="Test Space",
            description="This is a test space.",
            owner=self.user,
        )

    def test_grant_permission_view(self):
        member = User.objects.create_user(username="testmember", email="testmember@gmail.com", password="password")
        self.client.login(username="testuser", password="password")
        response = self.client.post(reverse("grant_permission", args=[self.space.pk, member.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertIn(member, self.space.granted_members.all())
        self.assertNotIn(member, self.space.members.all())

    def test_ungrant_permission_view(self):
        member = User.objects.create_user(username="testmember", email="testmember@gmail.com", password="password")
        self.space.granted_members.add(member)
        self.client.login(username="testuser", password="password")
        response = self.client.post(reverse("ungrant_permission", args=[self.space.pk, member.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertNotIn(member, self.space.granted_members.all())
        self.assertIn(member, self.space.members.all())

    def test_remove_member_view(self):
        member = User.objects.create_user(username="testmember", email="testmember@gmail.com", password="password")
        self.space.members.add(member)
        self.client.login(username="testuser", password="password")
        response = self.client.post(reverse("remove_member", args=[self.space.pk, member.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertNotIn(member, self.space.granted_members.all())
        self.assertNotIn(member, self.space.members.all())

    def test_make_moderator_view(self):
        member = User.objects.create_user(username="testmember", email="testmember@gmail.com", password="password")
        self.space.members.add(member)
        self.client.login(username="testuser", password="password")
        response = self.client.post(reverse("make_moderator", args=[self.space.pk, member.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertIn(member, self.space.moderators.all())
        self.assertNotIn(member, self.space.members.all())
        self.assertNotIn(member, self.space.granted_members.all())

    def test_join_space_view(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("join_space", args=[self.space.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.user, self.space.members.all())

    def test_my_spaces_list_authenticated(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("my_spaces_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "my_spaces_list.html")
        self.assertIn(self.space, response.context["spaces"])

    def test_delete_space_view(self):
        self.client.login(username="testuser", password="password")
        response = self.client.post(reverse("delete_space", args=[self.space.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Space.objects.filter(pk=self.space.pk).exists())

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
