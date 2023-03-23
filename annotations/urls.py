from django.urls import path
from . import views

urlpatterns = [
    path('annotations/', views.web_annotations_list, name='web-annotations-list'),
]