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
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(
        default="blank-profile-photo.jpeg",
        null=True,
        upload_to="users/%Y/%m/%d/",
        blank=True,
    )
    following = models.ManyToManyField("User", related_name="followers", verbose_name=_("Following"), blank=True)
    bookmarks = models.ManyToManyField(
        "posts.Post", related_name="bookmarked_posts", verbose_name=_("Bookmarked Posts"), blank=True
    )

    objects = UserManager()

    def __str__(self):
        return f"{self.username}"

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("user_detail", kwargs={"username": self.username})

    # @property
    # def followers(self):
    #     self.followers.all()
