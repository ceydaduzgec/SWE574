from annotations.models import Annotation
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .serializers import AnnotationSerializer


class AnnotationViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.annotation1 = Annotation.objects.create(
            id="test1",
            context="http://www.w3.org/ns/anno.jsonld",
            type="Annotation",
            body="http://example.com/1",
            target="http://example.com/2",
        )
        self.annotation2 = Annotation.objects.create(
            id="test2",
            context="http://www.w3.org/ns/anno.jsonld",
            type="Annotation",
            body="http://example.com/3",
            target="http://example.com/4",
        )

    def test_create_annotation(self):
        url = reverse("annotations")
        data = {
            "id": "test3",
            "context": "http://www.w3.org/ns/anno.jsonld",
            "type": "Annotation",
            "body": "http://example.com/5",
            "target": "http://example.com/6",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Annotation.objects.count(), 3)
        self.assertEqual(Annotation.objects.get(id="test3").body, "http://example.com/5")

    def test_get_annotation(self):
        url = reverse("annotations")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_single_annotation(self):
        url = reverse("annotation_detail", args=[self.annotation1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["body"], "http://example.com/1")

    def test_delete_annotation(self):
        url = reverse("annotation_detail", args=[self.annotation1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Annotation.objects.count(), 1)


class AnnotationSearchTestCase(TestCase):
    def setUp(self):
        self.annotation1 = Annotation.objects.create(
            id="http://example.org/anno1",
            body={"type": "TextualBody", "value": "This is the first annotation."},
            target={"source": "http://example.com/page1", "selector": {"type": "CssSelector", "value": ".section1"}},
        )
        self.annotation2 = Annotation.objects.create(
            id="http://example.org/anno2",
            body={"type": "TextualBody", "value": "This is the second annotation."},
            target={"source": "http://example.com/page1", "selector": {"type": "CssSelector", "value": ".section2"}},
        )

    def test_search_annotation_with_query(self):
        url = reverse("annotation_search")
        response = self.client.get(url, {"query": "second"})
        self.assertEqual(response.status_code, 200)

        serializer = AnnotationSerializer([self.annotation2], many=True)
        self.assertEqual(response.data, serializer.data)

    def test_search_annotation_without_query(self):
        url = reverse("annotation_search")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)

        expected_data = {"error": "Missing query parameter"}
        self.assertEqual(response.json(), expected_data)
