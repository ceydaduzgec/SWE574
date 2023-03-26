from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Annotation
from .serializers import AnnotationSerializer


class AnnotationViewSet(viewsets.ModelViewSet):
    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = Annotation.objects.all()
        annotation = get_object_or_404(queryset, pk=pk)
        serializer = AnnotationSerializer(annotation)
        return Response(serializer.data)

    def update(self, request, pk=None, *args, **kwargs):
        queryset = Annotation.objects.all()
        annotation = get_object_or_404(queryset, pk=pk)
        serializer = AnnotationSerializer(annotation, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        queryset = Annotation.objects.all()
        annotation = get_object_or_404(queryset, pk=pk)
        annotation.delete()
        return Response(status=204)
