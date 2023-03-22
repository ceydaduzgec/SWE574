from django import forms
from django.contrib.auth import get_user_model
from django.db.models import Q

from posts.models import Comment, Post
from spaces.models import Space
from users.models import Profile

User = get_user_model()


class PostForm(forms.ModelForm):
    spaces = forms.ModelMultipleChoiceField(queryset=Space.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields["spaces"].queryset = Space.objects.filter(
                Q(owner=user)
                | Q(moderators=user)
                | (Q(members=user) & Q(posting_permission="all"))
                | Q(granted_members=user)
            )

    class Meta:
        model = Post
        fields = ("title", "link", "tags", "labels", "text", "upload", "image", "spaces")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)


class EmailPostForm(forms.Form):
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("date_of_birth", "photo")
