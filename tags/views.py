from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view

from .models import Tag
from .serializers import TagSerializer
from .utils import get_wikidata_info


@api_view(["POST"])
def fetch_and_store_tag(request):
    wikidata_id = request.data.get("wikidata_id")
    if not wikidata_id:
        return JsonResponse({"error": "Missing Wikidata ID."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        tag = Tag.objects.get(wikidata_id=wikidata_id)
    except Tag.DoesNotExist:
        wikidata_info = get_wikidata_info(wikidata_id)
        if not wikidata_info:
            return JsonResponse({"error": "Unable to fetch data from Wikidata."}, status=status.HTTP_400_BAD_REQUEST)

        tag = Tag.objects.create(wikidata_id=wikidata_id, **wikidata_info)

    serializer = TagSerializer(tag)
    return JsonResponse(serializer.data, safe=False)


def index(request):
    return render(request, "index.html")
