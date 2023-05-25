from django import forms
from django.contrib.auth import get_user_model
from django.db.models import Q
from posts.models import Comment, Post, TagDescription
from spaces.models import Space

User = get_user_model()


class PostForm(forms.ModelForm):
    spaces = forms.ModelMultipleChoiceField(queryset=Space.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        selected_space = kwargs.pop("selected_space", None)
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            spaces = Space.objects.filter(
                Q(owner=user)
                | Q(moderators=user)
                | (Q(members=user) & Q(posting_permission="all"))
                | Q(granted_members=user)
            )
            if selected_space:
                spaces = spaces.filter(pk=selected_space.pk)
            self.fields["spaces"].queryset = spaces

    class Meta:
        model = Post
        fields = ("title", "link", "tags", "labels", "text", "upload", "image", "spaces")


class TagDescriptionForm(forms.ModelForm):
    class Meta:
        model = TagDescription
        fields = (
            "tag",
            "description",
        )


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
        fields = ("username", "email", "photo")
