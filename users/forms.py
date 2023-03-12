from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.contrib.auth import get_user_model


User = get_user_model()

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user


class UserEditForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):

	class Meta:
		model = Profile
		fields = ('date_of_birth', 'photo')