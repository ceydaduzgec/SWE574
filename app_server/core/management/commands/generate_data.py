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
            "Book Club",
            "Travel Enthusiasts",
            "Fitness Gurus",
            "Game Developers",
            "Photography",
            "Cooking Tips",
        ]

        users = User.objects.all()
        existing_space_names = Space.objects.values_list("name", flat=True)

        for name in space_names:
            if name not in existing_space_names:
                space = Space.objects.create(name=name, owner=random.choice(users))
                space.members.set(users)
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
                "tags": "cats, memes, funny",
            },
            {
                "title": "The latest smartphone for tech geeks",
                "content": "A review of the newest smartphone model that every tech geek should know about.",
                "space_name": "Tech Geeks",
                "link": "https://www.howtogeek.com/734936/best-android-phones/",
                "tags": "tech, smartphones, android",
            },
            {
                "title": "The ultimate pizza recipe",
                "content": "Discover the ultimate pizza recipe that will impress all pizza lovers.",
                "space_name": "Pizza Lovers",
                "link": "https://tasty.co/recipe/ultimate-homemade-pizza",
                "tags": "pizza, recipes, food",
            },
            {
                "title": "How to make the perfect cold brew",
                "content": "Learn how to make the perfect cold brew coffee at home with this step-by-step guide.",
                "space_name": "Coffee Addicts",
                "link": "https://cooking.nytimes.com/recipes/1017355-cold-brewed-iced-coffee",
                "tags": "coffee, recipes, drinks",
            },
            {
                "title": "The best books of 2021",
                "content": "Check out the best books of 2021 that every book lover should read.",
                "space_name": "Book Club",
                "link": "https://www.goodreads.com/choiceawards/best-books-2021",
                "tags": "books, reading, literature",
            },
            {
                "title": "The best travel destinations in Europe",
                "content": "Discover the best travel destinations in Europe that every travel enthusiast should visit.",
                "space_name": "Travel Enthusiasts",
                "link": "https://www.cntraveler.com/galleries/2015-07-07/top-10-cities-in-europe-readers-choice-awards-2015",
                "tags": "travel, europe, destinations",
            },
            {
                "title": "The best fitness apps",
                "content": "Check out the best fitness apps that will help you stay in shape.",
                "space_name": "Fitness Gurus",
                "link": "https://www.healthline.com/health/fitness-exercise/top-iphone-android-apps",
                "tags": "fitness, tech, health",
            },
            {
                "title": "The best game development tools",
                "content": "Discover the best game development tools that every game developer should know about.",
                "space_name": "Game Developers",
                "link": "https://www.gamedesigning.org/career/tools/",
                "tags": "game development, tech, programming",
            },
            {
                "title": "The best photography tips",
                "content": "Check out the best photography tips that will help you take amazing photos.",
                "space_name": "Photography",
                "link": "https://www.techradar.com/how-to/photography-video-capture/cameras/77-photography-techniques-tips-and-tricks-for-taking-pictures-of-anything-1320775",
                "tags": "photography, tips, art",
            },
            {
                "title": "The best cooking tips",
                "content": "Discover the best cooking tips that will help you become a better cook.",
                "space_name": "Cooking Tips",
                "link": "https://www.bbcgoodfood.com/howto/guide/top-10-cooking-tips",
                "tags": "cooking, tips, food",
            },
        ]

        for post_data in posts_data:
            space = Space.objects.filter(name=post_data["space_name"]).first()
            if space:
                if not Post.objects.filter(title=post_data["title"]).exists():
                    post = Post(
                        author=random.choice(User.objects.all()),
                        title=post_data["title"],
                        text=post_data["content"],
                        link=post_data["link"],
                    )
                    post.save()
                    post.spaces.add(space)
                    post.tags.add(*post_data["tags"].split(", "))

        print("Mock data created.")
