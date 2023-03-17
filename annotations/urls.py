from django.urls import path
from .views import AnnotationListCreateAPIView, AnnotationRetrieveUpdateDestroyAPIView


urlpatterns = [
    path('', AnnotationListCreateAPIView.as_view(), name='annotation-list-create'),
    path('<int:pk>/', AnnotationRetrieveUpdateDestroyAPIView.as_view(), name='annotation-retrieve-update-destroy'),
]
