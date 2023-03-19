# in urls.py

from django.urls import path
from .views import AnnotationCreateView, AnnotationListView


urlpatterns = [
    path(
        "annotations/create/", AnnotationCreateView.as_view(), name="annotation_create"
    ),
    path("annotations/", AnnotationListView.as_view(), name="annotation_list"),
]
