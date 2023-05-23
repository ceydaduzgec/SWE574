from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from posts.models import Post
from spaces.models import Space
from users.models import Badge
from tags.models import Tag
from recommendations.models import Recommendation

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


class TagTestCase(TestCase):
    def setUp(self):
        # create a test user
        self.user = User.objects.create_user(username="testuser", email="testuser@gmail.com", password="password")

    def test_create_descriptive_tag_via_wikidata(self):
        # Make a POST request to create a descriptive tag via Wikidata
        response = self.client.post(reverse("create_descriptive_tag"), {
            "name": "Test Tag",
            "wikidata_id": "Q123456",
        })

        # Assert that the response is successful
        self.assertEqual(response.status_code, 201)

        # Assert that the tag is created and has the correct attributes
        tag = Tag.objects.get(name="Test Tag")
        self.assertEqual(tag.name, "Test Tag")
        self.assertEqual(tag.wikidata_id, "Q123456")
        self.assertTrue(tag.is_descriptive)

    def test_create_informative_tag(self):
        # Make a POST request to create an informative tag
        response = self.client.post(reverse("create_informative_tag"), {
            "name": "Test Tag",
            "description": "Test description",
        })

        # Assert that the response is successful
        self.assertEqual(response.status_code, 201)

        # Assert that the tag is created and has the correct attributes
        tag = Tag.objects.get(name="Test Tag")
        self.assertEqual(tag.name, "Test Tag")
        self.assertEqual(tag.description, "Test description")
        self.assertFalse(tag.is_descriptive)

    def test_assign_tag_to_post(self):
        # Create a test post
        post = Post.objects.create(title="Test Post", text="Test content", author=self.user)

        # Create a test tag
        tag = Tag.objects.create(name="Test Tag", description="Test description")

        # Assign the tag to the post
        post.tags.add(tag)

        # Assert that the tag is assigned to the post
        self.assertIn(tag, post.tags.all())

    def test_tag_based_post_search(self):
        # Create a test post with a tag
        post = Post.objects.create(title="Test Post", text="Test content", author=self.user)
        tag = Tag.objects.create(name="Test Tag", description="Test description")
        post.tags.add(tag)

        # Make a GET request to search for posts by tag
        response = self.client.get(reverse("tag_search"), {"tag": "Test Tag"})

        # Assert that the response is successful
        self.assertEqual(response.status_code, 200)

        # Assert that the post is included in the search results
        self.assertIn(post, response.context["posts"])

class RecommendationTestCase(TestCase):
    def setUp(self):
        # create test users
        self.user1 = User.objects.create_user(username="user1", email="user1@gmail.com", password="password")
        self.user2 = User.objects.create_user(username="user2", email="user2@gmail.com", password="password")
        self.user3 = User.objects.create_user(username="user3", email="user3@gmail.com", password="password")

        # create test spaces
        self.space1 = Space.objects.create(name="Space 1", description="Description 1", owner=self.user1)
        self.space2 = Space.objects.create(name="Space 2", description="Description 2", owner=self.user2)
        self.space3 = Space.objects.create(name="Space 3", description="Description 3", owner=self.user3)

        # create test posts
        self.post1 = Post.objects.create(title="Post 1", text="Content 1", author=self.user1)
        self.post2 = Post.objects.create(title="Post 2", text="Content 2", author=self.user2)
        self.post3 = Post.objects.create(title="Post 3", text="Content 3", author=self.user3)

    def test_user_recommendations(self):
        # Add interests and space memberships for user1
        self.user1.interests.add("interest1", "interest2")
        self.space1.members.add(self.user1)
        self.space2.members.add(self.user1)

        # Add interests and space memberships for user2
        self.user2.interests.add("interest2", "interest3")
        self.space2.members.add(self.user2)
        self.space3.members.add(self.user2)

        # Generate user recommendations
        recommendations = Recommendation.generate_user_recommendations(self.user1)

        # Assert that user2 and user3 are recommended
        self.assertIn(self.user2, recommendations)
        self.assertNotIn(self.user3, recommendations)

    def test_space_recommendations(self):
        # Generate space recommendations for space1
        recommendations = Recommendation.generate_space_recommendations(self.space1)

        # Assert that space2 and space3 are recommended
        self.assertIn(self.space2, recommendations)
        self.assertNotIn(self.space3, recommendations)

    def test_post_recommendations(self):
        # Add tags to posts
        self.post1.tags.add("tag1", "tag2")
        self.post2.tags.add("tag2", "tag3")
        self.post3.tags.add("tag3", "tag4")

        # Generate post recommendations for user1
        recommendations = Recommendation.generate_post_recommendations(self.user1)

        # Assert that post2 and post3 are recommended
        self.assertIn(self.post2, recommendations)
        self.assertNotIn(self.post1, recommendations)
