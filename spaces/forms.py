from django import forms
from django.contrib.auth import get_user_model

from spaces.models import Space

from .models import Interest

User = get_user_model()


class InterestForm(forms.Form):
    interest = forms.ModelChoiceField(queryset=Interest.objects.all(), empty_label="Select an interest", required=False)


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
        fields = ["posting_permission"]
        widgets = {
            "posting_permission": forms.RadioSelect(attrs={"class": "form-check-input"}),
        }
        labels = {
            "posting_permission": "Posting Permission",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["posting_permission"].choices = POSTING_PERMISSION_CHOICES
