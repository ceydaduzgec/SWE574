from rest_framework import serializers

from .models import Annotation


class AnnotationSerializer(serializers.ModelSerializer):
    context = serializers.SerializerMethodField()

    def get_context(self, instance):
        return "http://www.w3.org/ns/anno.jsonld"

    class Meta:
        model = Annotation
        fields = ["id", "context", "type", "body", "target", "creation_datetime"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["@context"] = data.pop("context")
        return data
