from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import Client, TestCase
from django.urls import reverse
from users.forms import NewUserForm, UserEditForm
from users.tests.factories import UserFactory

User = get_user_model()


class UserAccountTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = UserFactory(
            email="testuser@super.com",
            username="johnnyjoe",
            first_name="Joe",
            password="aad3fa",
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )

    def tearDown(self):
        super().tearDown()

    def test_new_superuser(self):
        self.assertEqual(self.user.email, "testuser@super.com")
        self.assertEqual(self.user.username, "johnnyjoe")
        self.assertEqual(self.user.first_name, "Joe")
        self.assertTrue(self.user.is_superuser)
        self.assertTrue(self.user.is_staff)
        self.assertTrue(self.user.is_active)
        self.assertEqual(str(self.user), "johnnyjoe")

    def test_new_user(self):
        self.user.is_active = False
        self.user.is_superuser = False
        self.user.is_staff = False
        self.user.save(update_fields=["is_active", "is_superuser", "is_staff"])

        self.assertFalse(self.user.is_superuser)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_active)

    def test_empty_fields(self):
        with self.assertRaisesMessage(ValidationError, "'password': ['This field cannot be blank.']"):
            self.user.password = ""
            self.user.save(update_fields=["password"])

        with self.assertRaisesMessage(ValidationError, "'email': ['This field cannot be blank.']"):
            self.user.email = ""
            self.user.save(update_fields=["email"])

        with self.assertRaisesMessage(ValidationError, "'username': ['This field cannot be blank.']"):
            self.user.username = ""
            self.user.save(update_fields=["username"])

    def test_username_regex(self):
        with self.assertRaisesMessage(
            ValidationError,
            "'username': ['Username is invalid. Only lowercase English letters, period and underscore characters are allowed. Minimum length is three characters.']",
        ):
            self.user.username = "ASDSA"
            self.user.save(update_fields=["username"])

        with self.assertRaisesMessage(
            ValidationError,
            "'username': ['Username is invalid. Only lowercase English letters, period and underscore characters are allowed. Minimum length is three characters.']",
        ):
            self.user.username = "ae"
            self.user.save(update_fields=["username"])

        with self.assertRaisesMessage(
            ValidationError,
            "'username': ['Username is invalid. Only lowercase English letters, period and underscore characters are allowed. Minimum length is three characters.']",
        ):
            self.user.username = "asd?=-"
            self.user.save(update_fields=["username"])

    def test_unique_fields(self):
        with self.assertRaisesMessage(ValidationError, "'email': ['User with this Email already exists.']"):
            UserFactory(
                email="testuser@super.com",
                username="josy",
                first_name="Josh",
                password="asdsad",
            )
        with self.assertRaisesMessage(ValidationError, "'username': ['User with this Username already exists.']"):
            UserFactory(
                email="tesfs@user.com",
                username="johnnyjoe",
                first_name="Josh",
                password="asdsad",
            )

    def test_absolute_url(self):
        self.assertEqual(self.user.get_absolute_url(), "/users/johnnyjoe/")


class UserEditTestCase(TestCase):
    def setUp(cls):
        cls.user = UserFactory()
        cls.form_data = {"first_name": "tester", "last_name": "joe", "email": "tester@gmail.com", "username": "tester"}

    def test_form_update(self):
        form = UserEditForm(self.form_data, instance=self.user)
        form.save()
        self.assertTrue(form.is_valid())
        self.user.refresh_from_db()
        self.assertTrue(self.user.first_name, "tester")
        self.assertTrue(self.user.last_name, "joe")
        self.assertTrue(self.user.email, "tester@gmail.com")


class NewUserTestCase(TestCase):
    def setUp(cls):
        cls.form_data = {
            "username": "user",
            "email": "tester@gmail.com",
            "password1": "123asd.FGH",
            "password2": "123asd.FGH",
        }

    def test_valid_form(self):
        form = NewUserForm(self.form_data)
        form.save()
        self.assertTrue(form.is_valid())

        user = User.objects.get(username="user")
        self.assertTrue(user.username, "tester")
        self.assertTrue(user.email, "tester@gmail.com")

    def test_invalid_form(self):
        with self.assertRaisesMessage(
            ValueError,
            "The User could not be created because the data didn't validate.",
        ):
            form = NewUserForm(self.form_data)
            form.data["password1"] = "pass"
            form.data["password2"] = "pass"
            self.assertFalse(form.is_valid())
            self.assertEqual(
                form.errors,
                {
                    "password2": [
                        "This password is too short. It must contain at least 8 characters.",
                        "This password is too common.",
                    ]
                },
            )
            form.save()


class UserAuthenticationTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def user_creation(self):
        self.user = User.objects.create_user(username="testuser", email="test@gmail.com", password="password")
        found_user = User.objects.filter(username="testuser", email="test@gmail.com", password="password")
        self.assertEqual(found_user.count(), 1)

    def test_user_registration(self):
        # Make a POST request to register a new user
        response = self.client.post(
            reverse("register"),
            {
                "username": "testuser",
                "email": "test@gmail.com",
                "password1": "password",
                "password2": "password",
            },
        )

        # Check that the user was created successfully
        self.assertEqual(response.status_code, 200)
        found_user = User.objects.filter(username="testuser", email="test@gmail.com")
        self.assertEqual(found_user.count(), 1)

    def test_user_login(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", email="test@gmail.com", password="password")

        # Make a POST request to log in as the test user
        response = self.client.post(
            reverse("login"),
            {
                "username": "testuser",
                "password": "password",
            },
        )

        # Check that the login was successful
        self.assertEqual(response.status_code, 302)
        self.assertTrue("_auth_user_id" in self.client.session)
        self.assertEqual(int(self.client.session["_auth_user_id"]), self.user.id)


# class FollowViewTest(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = UserFactory()
#         self.user2 = UserFactory()

#     def test_follow_view(self):
#         self.client.force_login(self.user)
#         url = reverse("user_follow")
#         data = {"id": self.user2.id, "action": "follow"}
#         response = self.client.post(url, data=data)
#         self.assertEqual(response.status_code, 200)
#         self.assertTrue(self.user.following.filter(pk=self.user2.id).exists())

#     def test_unfollow_view(self):
#         self.client.force_login(self.user)
#         self.user.following.add(self.user2)
#         url = reverse("user_follow")
#         data = {"id": self.user2.id, "action": "unfollow"}
#         response = self.client.post(url, data=data)
#         self.assertEqual(response.status_code, 200)
#         self.assertFalse(self.user.following.filter(pk=self.user2.id).exists())
