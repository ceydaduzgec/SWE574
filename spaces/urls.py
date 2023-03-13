from django.urls import path

from spaces.views import create_space, space_detail, space_list

urlpatterns = [
    path("spaces/", space_list, name="space_list"),
    path("spaces/new/", create_space, name="create_space"),
    path("spaces/<int:pk>/", space_detail, name="space_detail"),
]
