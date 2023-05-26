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
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    link = models.URLField(max_length=200, blank=True, unique=False)
    tags = TaggableManager(blank=True)
    tag_descriptions = models.ManyToManyField("TagDescription", blank=True)
    labels = models.CharField(max_length=200, blank=True)
    text = models.CharField(max_length=2000, blank=True)
    upload = models.FileField(upload_to="uploads/", null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    likes = models.ManyToManyField(User, blank=True, related_name="liked_posts")
    title_tag = models.CharField(max_length=200, null=True, blank=True, unique=False)
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    spaces = models.ManyToManyField("spaces.Space", related_name="posts", blank=True)
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

    def _str_(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", args=[self.id])


class TagDescription(models.Model):
    tag = models.ForeignKey("taggit.Tag", on_delete=models.CASCADE, related_name="tag_description")
    description = models.CharField(max_length=200, blank=True, unique=False)

    def _str_(self):
        return f"{self.tag.name}: {self.description}"


class Comment(models.Model):
    post = models.ForeignKey("posts.Post", on_delete=models.CASCADE, related_name="comments")
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

    def _str_(self):
        return self.text


class ReportedPost(models.Model):
    post = models.ForeignKey("posts.Post", on_delete=models.CASCADE, related_name="reports")
    reported_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
