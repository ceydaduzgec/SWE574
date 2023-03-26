import factory
from django.core.files.uploadedfile import SimpleUploadedFile

from posts.models import Post
from spaces.tests.factories import SpaceFactory
from users.tests.factories import UserFactory


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    author = factory.SubFactory(UserFactory)
    title = factory.fuzzy.FuzzyText(length=10)
    link = factory.Faker("url")
    tags = None
    labels = factory.fuzzy.FuzzyText(length=100)
    text = factory.fuzzy.FuzzyText(length=100)
    upload = factory.LazyAttribute(
        lambda o: SimpleUploadedFile(name="image.jpg", content=b"", content_type="image/jpeg")
    )
    # created_date = factory.fuzzy.FuzzyDateTime(datetime.datetime(2023, 3, 1, tzinfo=datetime.timezone.utc))
    # published_date = factory.fuzzy.FuzzyDateTime(datetime.datetime(2023, 6, 1, tzinfo=datetime.timezone.utc))
    title_tag = factory.fuzzy.FuzzyText(length=100)
    image = factory.LazyAttribute(
        lambda o: SimpleUploadedFile(name="image.jpg", content=b"", content_type="image/jpeg")
    )

    @factory.post_generation
    def likes(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for object in extracted:
                self.likes.add(object)
        else:
            for _ in range(2):
                self.likes.add(UserFactory())

    @factory.post_generation
    def spaces(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for object in extracted:
                self.spaces.add(object)
        else:
            for _ in range(2):
                self.spaces.add(SpaceFactory())
