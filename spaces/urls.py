from django.urls import path
from spaces.views import create_space, space_detail, space_list, my_spaces_list, space_policies

urlpatterns = [
    path("spaces/", space_list, name="space_list"),
    path("spaces/new/", create_space, name="create_space"),
    path("spaces/<int:pk>/", space_detail, name="space_detail"),
    path("spaces/myspaces/", my_spaces_list, name="my_spaces_list"),
    path("spaces/<int:pk>/policies/", space_policies, name="space_policies"),

]
