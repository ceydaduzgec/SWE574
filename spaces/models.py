from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class Space(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_spaces")
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
