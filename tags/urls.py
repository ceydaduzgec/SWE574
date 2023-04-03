from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("tags/fetch_and_store/", views.fetch_and_store_tag, name="fetch_and_store_tag"),
]
