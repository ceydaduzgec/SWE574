# in urls.py

from django.urls import path, re_path

from .views import AnnotationDetail, AnnotationList

urlpatterns = [
    path("", AnnotationList.as_view(), name="annotations"),
    re_path(r"^(?P<pk>[\w:/.#?!\-]+)/$", AnnotationDetail.as_view(), name="annotation_detail"),
]
