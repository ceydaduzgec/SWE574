from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ClearableFileInput, ImageField

User = get_user_model()


class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class CustomClearableFileInput(ClearableFileInput):
    initial_text = "Current"
    input_text = "Change"
    clear_checkbox_label = ""  # this is the line that removes the "Clear checkbox" text


class UserEditForm(forms.ModelForm):
    photo = ImageField(widget=CustomClearableFileInput)  # override the photo field

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "bio", "email", "photo")
