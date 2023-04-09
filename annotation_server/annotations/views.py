from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Annotation
from .serializers import AnnotationSerializer


class AnnotationView(APIView):
    """
    API endpoint that allows Annotations to be created, updated, and deleted.
    """

    def post(self, request):
        serializer = AnnotationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, pk):
        try:
            return Annotation.objects.get(pk=pk)
        except Annotation.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        annotation = self.get_object(pk)
        serializer = AnnotationSerializer(annotation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        annotation = self.get_object(pk)
        annotation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, pk=None):
        if pk:
            annotation = self.get_object(pk)
            serializer = AnnotationSerializer(annotation)
            return Response(serializer.data)
        else:
            annotations = Annotation.objects.all()
            serializer = AnnotationSerializer(annotations, many=True)
            return Response(serializer.data)
