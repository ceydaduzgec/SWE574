from django.contrib.auth import get_user_model
from factory import Faker
from factory.django import DjangoModelFactory

User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = Faker("email")
    username = Faker("user_name")
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    password = Faker("password")
    is_active = True
    is_staff = False
    is_superuser = False
    date_of_birth = Faker("date_of_birth")
    bio = Faker("text", max_nb_chars=200)
