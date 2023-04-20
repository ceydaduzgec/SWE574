from django.core.management import BaseCommand

from spaces.models import Space
from users.tests.factories import UserFactory


class Command(BaseCommand):
    help = "Creates a random local data for testing."

    def handle(self, *args, **kwargs):
        for _ in range(10):
            UserFactory()

        spaces = [
            Space(name="Cat Memes"),
            Space(name="Tech Geeks"),
            Space(name="Pizza Lovers"),
            Space(name="Coffee Addicts"),
        ]
        Space.objects.bulk_create(spaces)

        print("Mock data created.")
