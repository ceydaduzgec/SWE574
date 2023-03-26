from django.core.exceptions import ValidationError
from django.test import TestCase

from users.forms import UserEditForm
from users.tests.factories import UserFactory


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
        cls.form_data = {"first_name": "tester", "last_name": "joe", "email": "tester@gmail.com"}

    def test_form_update(self):
        form = UserEditForm(self.form_data, instance=self.user)
        form.save()
        self.assertTrue(form.is_valid())
        self.user.refresh_from_db()
        self.assertTrue(self.user.first_name, "tester")
        self.assertTrue(self.user.last_name, "joe")
        self.assertTrue(self.user.email, "tester@gmail.com")
