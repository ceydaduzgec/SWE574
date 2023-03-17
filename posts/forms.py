from django import forms
from django.contrib.auth import get_user_model

from posts.models import Comment, Post
from users.models import Profile

User = get_user_model()


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "link", "tags", "labels", "upload", "text", "image")


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
