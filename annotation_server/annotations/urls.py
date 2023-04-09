# in urls.py

from django.urls import path

from .views import AnnotationView

urlpatterns = [
    path("", AnnotationView.as_view(), name="annotations"),
]
