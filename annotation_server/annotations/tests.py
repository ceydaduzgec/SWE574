from django.test import TestCase

from .models import Annotation


class AnnotationModelTest(TestCase):
    def test_as_dict_method(self):
        annotation = Annotation(
            id="http://example.org/anno1",
            type="Annotation",
            body={"type": "TextualBody", "value": "Test annotation"},
            target={
                "source": "http://example.org/document1",
                "selector": {"type": "FragmentSelector", "value": "page=2"},
            },
        )
        expected_dict = {
            "@context": "http://www.w3.org/ns/anno.jsonld",
            "id": "http://example.org/anno1",
            "type": "Annotation",
            "body": {"type": "TextualBody", "value": "Test annotation"},
            "target": {
                "source": "http://example.org/document1",
                "selector": {"type": "FragmentSelector", "value": "page=2"},
            },
        }
        self.assertEqual(annotation.as_dict(), expected_dict)
