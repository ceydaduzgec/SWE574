import random

from django.core.management import BaseCommand
from faker import Faker
from posts.models import Post
from spaces.models import Space
from users.models import User
from users.tests.factories import UserFactory


class Command(BaseCommand):
    help = "Creates a random local data for testing."

    def handle(self, *args, **kwargs):
        for _ in range(10):
            UserFactory()

        space_names = [
            "Cat Memes",
            "Tech Geeks",
            "Pizza Lovers",
            "Coffee Addicts",
        ]

        users = User.objects.all()

        for name in space_names:
            space, _ = Space.objects.get_or_create(name=name, owner=random.choice(users))
            space.members.add(*users)
            space.moderators.add(random.choice(users))
            space.save()

        spaces = Space.objects.all()

        fake = Faker()

        for _ in range(4):
            user = User(
                email=fake.email(),
                username=fake.user_name(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                password=fake.password(),
                is_active=True,
                is_staff=False,
                is_superuser=False,
            )
            user.save()

        for space in spaces:
            if random.random() < 0.5:
                user = random.choice(User.objects.all())
                space.members.add(user)
                space.moderators.add(user)
                space.save()

        # Create posts with your specified data
        posts_data = [
            {
                "title": "Funny cat memes compilation",
                "content": "Check out this hilarious compilation of cat memes that will make your day.",
                "space_name": "Cat Memes",
                "link": "https://www.youtube.com/watch?v=LuYsO5DgLrc",
            },
            {
                "title": "The latest smartphone for tech geeks",
                "content": "A review of the newest smartphone model that every tech geek should know about.",
                "space_name": "Tech Geeks",
                "link": "https://www.howtogeek.com/734936/best-android-phones/",
            },
            {
                "title": "The ultimate pizza recipe",
                "content": "Discover the ultimate pizza recipe that will impress all pizza lovers.",
                "space_name": "Pizza Lovers",
                "link": "https://tasty.co/recipe/ultimate-homemade-pizza",
            },
            {
                "title": "How to make the perfect cold brew",
                "content": "Learn how to make the perfect cold brew coffee at home with this step-by-step guide.",
                "space_name": "Coffee Addicts",
                "link": "https://cooking.nytimes.com/recipes/1017355-cold-brewed-iced-coffee",
            },
        ]

        for post_data in posts_data:
            space = Space.objects.filter(name=post_data["space_name"]).first()
            if space:
                post = Post(
                    author=random.choice(User.objects.all()),
                    title=post_data["title"],
                    text=post_data["content"],
                    link=post_data["link"],
                )
                post.save()
                post.spaces.add(space)

        print("Mock data created.")
