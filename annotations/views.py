# views.py
from rest_framework import generics
from .models import Annotation
from .serializers import AnnotationSerializer


class AnnotationListCreateAPIView(generics.ListCreateAPIView):
    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer
    template_name = "annotations/templates/annotation_create.html"


class AnnotationRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer
