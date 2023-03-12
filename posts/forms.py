from django import forms
from .models import *
from authenticator.forms import *
from authenticator.models import Profile
from django import forms
from .models import Space
class SpaceCreationForm(forms.ModelForm):
    class Meta:
        model = Space
        fields = ['name', 'description', 'members', 'moderators', 'is_all_members_post_allowed', 'is_only_moderators_post_allowed']


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'link', 'tags', 'labels', 'upload', 'text', 'image' )

class SpaceForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'link', 'text')

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)

# class ProfileForm(forms.ModelForm):
#
#     class Meta:
#         model = Author
#         fields = '__all__'


class EmailPostForm(forms.Form):

    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')