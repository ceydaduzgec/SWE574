import requests
from django.core.exceptions import ValidationError
from rfc3987 import parse


def validate_iri(iri):
    try:
        parse(iri, rule="IRI")
    except ValueError:
        return ValidationError("The value does not conform to the IRI specification.")


def validate_annotation_type(type):
    response = requests.get("https://www.w3.org/ns/anno.jsonld")
    if response.status_code != 200:
        raise ValidationError("Failed to retrieve annotation JSON-LD schema.")
    annotation_jsonld = response.json()
    if type not in annotation_jsonld:
        raise ValidationError("The type is not a valid annotation JSON-LD property.")
