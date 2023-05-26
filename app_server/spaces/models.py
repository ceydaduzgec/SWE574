from collections import Counter

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class Space(models.Model):
    POSTING_PERMISSION_CHOICES = (
        ("all", "Any member can post"),
        ("granted", "Only granted members can post"),
        ("moderators", "Only moderators can post"),
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_spaces")
    name = models.CharField(max_length=200)
    description = models.TextField()
    members = models.ManyToManyField(User, related_name="spaces", blank=True)
    moderators = models.ManyToManyField(User, related_name="moderated_spaces", blank=True)
    posting_permission = models.CharField(choices=POSTING_PERMISSION_CHOICES, max_length=47, default="all")
    granted_members = models.ManyToManyField(User, related_name="granted_spaces", blank=True)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("-created_date",)

    def get_granted_members(self):
        return self.granted_members.all()

    def get_moderators(self):
        return self.moderators.all()

    def can_member_post(self, user):
        if self.posting_permission == "all":
            return (
                user in self.get_granted_members() or self.members.all() or self.get_moderators() or user == self.owner
            )
        elif self.posting_permission == "granted":
            return user in self.get_granted_members() or self.get_moderators() or user == self.owner
        elif self.posting_permission == "moderators":
            return user in self.get_moderators() or user == self.owner
        else:
            return False

    def update_tags_counter(self):
        posts = self.posts.all()
        tags_counter = Counter()
        for post in posts:
            tags_counter.update(post.tags.names())
        self.tags_counter = tags_counter
        self.save()

    def __str__(self):
        return self.name
