from django import forms
from django.contrib.auth import get_user_model

from posts.models import Post
from spaces.models import Space

User = get_user_model()


class SpaceCreationForm(forms.ModelForm):
    class Meta:
        model = Space
        fields = [
            "name",
            "description",
            "posting_permission",
        ]

POSTING_PERMISSION_CHOICES = (
    ("all", "Any member can post"),
    ("granted", "Only granted members can post"),
    ("moderators", "Only moderators can post"),
)

class SpacePolicyForm(forms.ModelForm):
    class Meta:
        model = Space
        fields = ["posting_permission", "granted_members"]
        widgets = {
            "posting_permission": forms.RadioSelect(attrs={"class": "form-check-input"}),
            "granted_members": forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),
        }
        labels = {
            "posting_permission": "Posting Permission",
            "granted_members": "Granted Members",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.posting_permission != "granted":
            self.fields["granted_members"].widget = forms.HiddenInput()
        self.fields["posting_permission"].choices = POSTING_PERMISSION_CHOICES
