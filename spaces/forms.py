from django import forms
from django.contrib.auth import get_user_model

from posts.models import Post, Space


User = get_user_model()


class SpaceCreationForm(forms.ModelForm):
    class Meta:
        model = Space
        fields = [
            "name",
            "description",
            "members",
            "moderators",
            "is_all_members_post_allowed",
            "is_only_moderators_post_allowed",
        ]


class SpaceForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "link", "text")
