from django.contrib.auth import views as auth_views
from django.urls import path

from users.views import (
    edit,
    login_request,
    logout_request,
    my_account,
    register_request,
    user_detail,
    user_follow,
    user_list,
)

urlpatterns = [
    path("register/", register_request, name="register"),
    path("login/", login_request, name="login"),
    path("logout", logout_request, name="logout"),
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
    path("edit/", edit, name="edit"),  # TODO: change name to more meaningful one
    path("users/", user_list, name="user_list"),
    path("users/<username>/", user_detail, name="user_detail"),
    path("users/follow", user_follow, name="user_follow"),
    path("myaccount/", my_account, name="my_account"),

]
