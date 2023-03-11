from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager

User = get_user_model()


class Post(models.Model):
    # STATUS_CHOICES = (
    #     ('draft', 'Draft'),
    #     ('published', 'Published'),
    # )
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True)
    link = models.CharField(max_length=200, null=True, blank=True, unique=False)
    tags = TaggableManager(blank=True)
    labels = models.CharField(max_length=200, blank=True)
    text = models.CharField(max_length=2000, blank=True)
    upload = models.FileField(upload_to="uploads/", null=True, blank=True, unique=False)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    likes = models.ManyToManyField(User, blank=True, related_name="blog_post")
    title_tag = models.CharField(max_length=200, null=True, blank=True, unique=False)
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    spaces = models.ManyToManyField("posts.Space", related_name="posts", blank=True)
    # status = models.CharField(max_length=10,
    #                           choices=STATUS_CHOICES,
    #                           default='draft')

    def total_likes(self):
        return self.likes.count()

    class Meta:
        ordering = ("-published_date",)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", args=[self.id])


class Comment(models.Model):
    post = models.ForeignKey(
        "posts.Post", on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    class Meta:
        ordering = ("created_date",)
        indexes = [
            models.Index(fields=["created_date"]),
        ]

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text


class Space(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owned_spaces"
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    members = models.ManyToManyField(User, related_name="spaces")
    moderators = models.ManyToManyField(User, related_name="moderated_spaces")
    is_all_members_post_allowed = models.BooleanField(default=True)
    is_only_moderators_post_allowed = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("-created_date",)

    def __str__(self):
        return self.name
