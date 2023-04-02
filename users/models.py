from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    username = models.CharField(
        _("Username"),
        max_length=150,
        unique=True,
        blank=False,
        validators=[
            RegexValidator(
                r"^[a-z0-9._]{3,}$",  # Only lowercase English letters, period and underscore characters are allowed. Minimum length is three characters.
                _(
                    "Username is invalid. Only lowercase English letters, period and underscore characters are allowed. Minimum length is three characters."
                ),
            )
        ],
    )
    email = models.EmailField(_("Email"), unique=True, blank=False)
    bio = models.TextField(_("Bio"), blank=True, null=False)
    followers = models.ManyToManyField(
        "User",
        through="Contact",
        related_name="follower_users",
        symmetrical=False,
        verbose_name=_("Followers"),
        blank=True,
    )
    following = models.ManyToManyField("User", related_name="following_users", verbose_name=_("Following"), blank=True)
    objects = UserManager()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("user_detail", kwargs={"username": self.username})


class Contact(models.Model):
    user_from = models.ForeignKey(User, related_name="rel_from_set", on_delete=models.CASCADE)
    user_to = models.ForeignKey(User, related_name="rel_to_set", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return f"{self.user_from} follows {self.user_to}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(
        default="blank-profile-photo.jpeg",
        null=True,
        upload_to="users/%Y/%m/%d/",
        blank=True,
    )

    def __str__(self):
        return f"Profile for user {self.user.username}"
