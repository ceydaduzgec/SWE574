from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(template_name="password_change_form.html"),
    ),
    path(
        "password_change/done/",  # TODO: check if done urls are necessary
        auth_views.PasswordChangeDoneView.as_view(template_name="password_change_done.html"),
    ),
    # reset password urls
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(template_name="password_reset_form.html"),
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"),
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"),
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"),
    ),
    path("edit/", views.edit, name="edit"),  # TODO: change name to more meaningful one
    path("users/", views.user_list, name="user_list"),
    path("users/<username>/", views.user_detail, name="user_detail"),
    path("users/follow", views.user_follow, name="user_follow"),
]
