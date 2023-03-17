from django.urls import path

from spaces.views import (
    create_space,
    my_spaces_list,
    space_detail,
    space_list,
    space_policies,
    space_members,
    join_space,
    leave_space,
)

urlpatterns = [
    path("spaces/", space_list, name="space_list"),
    path("spaces/new/", create_space, name="create_space"),
    path("spaces/<int:pk>/", space_detail, name="space_detail"),
    path("spaces/myspaces/", my_spaces_list, name="my_spaces_list"),
    path("spaces/<int:pk>/policies/", space_policies, name="space_policies"),
    path("spaces/<int:pk>/members/", space_members, name="space_members"),
    path("spaces/<int:pk>/join/", join_space, name="join_space"),
    path("spaces/<int:pk>/leave/", leave_space, name="leave_space"),

]
