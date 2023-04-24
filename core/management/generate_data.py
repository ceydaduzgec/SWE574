from django.core.management import BaseCommand

from spaces.models import Space
from posts.models import Post
from users.models import User
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

for space in spaces:
    space.save()

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
        if random.random() < 0.5:  # Adjust this probability to control how many spaces each user is assigned
            space.admins.add(user)
            space.save()

# Create posts with your specified data
posts_data = [
    {
        "title": "Funny cat memes compilation",
        "content": "Check out this hilarious compilation of cat memes that will make your day.",
        "space": Space.objects.get(name="Cat Memes"),
        "link": "https://www.youtube.com/watch?v=LuYsO5DgLrc",
    },
    {
        "title": "The latest smartphone for tech geeks",
        "content": "A review of the newest smartphone model that every tech geek should know about.",
        "space": Space.objects.get(name="Tech Geeks"),
        "link": "https://www.howtogeek.com/734936/best-android-phones/",
    },
    {
        "title": "The ultimate pizza recipe",
        "content": "Discover the ultimate pizza recipe that will impress all pizza lovers.",
        "space": Space.objects.get(name="Pizza Lovers"),
        "link": "https://tasty.co/recipe/ultimate-homemade-pizza",
    },
    {
        "title": "How to make the perfect cold brew",
        "content": "Learn how to make the perfect cold brew coffee at home with this step-by-step guide.",
        "space": Space.objects.get(name="Coffee Addicts"),
        "link": "https://cooking.nytimes.com/recipes/1017355-cold-brewed-iced-coffee",
    },
]

for post_data in posts_data:
    post = Post(
        author=random.choice(User.objects.all()),
        space=post_data["space"],
        title=post_data["title"],
        content=post_data["content"],
        link=post_data["link"],
    )
    post.save()
()