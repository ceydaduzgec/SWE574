import factory

from spaces.models import Space
from users.tests.factories import UserFactory


class SpaceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Space

    owner = factory.SubFactory(UserFactory)
    name = factory.fuzzy.FuzzyText(length=10)
    description = factory.fuzzy.FuzzyText(length=100)
    posting_permission = factory.fuzzy.FuzzyChoice(Space.POSTING_PERMISSION_CHOICES)
    # created_date = factory.fuzzy.FuzzyDateTime(datetime.datetime(2023, 3, 1, tzinfo=datetime.timezone.utc))

    @factory.post_generation
    def members(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for help in extracted:
                self.likes.add(help)
        else:
            for _ in range(2):
                self.likes.add(UserFactory())

    @factory.post_generation
    def moderators(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for help in extracted:
                self.likes.add(help)
        else:
            for _ in range(2):
                self.likes.add(UserFactory())

    @factory.post_generation
    def granted_members(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for help in extracted:
                self.likes.add(help)
        else:
            for _ in range(2):
                self.likes.add(UserFactory())
