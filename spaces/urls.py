from django.urls import path

from spaces.views import (
    create_space,
    delete_space,
    grant_permission,
    join_space,
    leave_space,
    make_moderator,
    my_spaces_list,
    newspace,
    remove_member,
    remove_moderator,
    space_detail,
    space_list,
    space_members,
    space_policies,
    ungrant_permission,
)

urlpatterns = [
    path("spaces/", space_list, name="space_list"),
    path("spaces/new/", create_space, name="create_space"),
    path("spaces/<int:pk>/delete/", delete_space, name="delete_space"),
    path("spaces/<int:pk>/", space_detail, name="space_detail"),
    path("spaces/myspaces/", my_spaces_list, name="my_spaces_list"),
    path("spaces/<int:pk>/policies/", space_policies, name="space_policies"),
    path("spaces/<int:pk>/members/", space_members, name="space_members"),
    path("spaces/<int:pk>/join/", join_space, name="join_space"),
    path("spaces/<int:pk>/leave/", leave_space, name="leave_space"),
    path("newspace/", newspace, name="newspace"),
    path("spaces/<int:space_pk>/members/<int:member_pk>/remove/", remove_member, name="remove_member"),
    path("spaces/<int:space_pk>/members/<int:member_pk>/make_moderator/", make_moderator, name="make_moderator"),
    path(
        "spaces/<int:space_pk>/members/<int:moderator_pk>/remove_moderator/", remove_moderator, name="remove_moderator"
    ),
    path("spaces/<int:space_pk>/members/<int:member_pk>/grant_permission/", grant_permission, name="grant_permission"),
    path(
        "spaces/<int:space_pk>/members/<int:member_pk>/ungrant_permission/",
        ungrant_permission,
        name="ungrant_permission",
    ),
]
