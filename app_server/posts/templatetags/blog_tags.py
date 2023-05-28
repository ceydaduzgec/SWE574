import json

from django import template

from ..models import Post

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.objects.filter(author=2).count()


@register.inclusion_tag("latest_posts.html")
def show_latest_posts(id, count=5):
    latest_posts = Post.objects.filter(author=2).order_by("-published_date")[:count]
    return {"latest_posts": latest_posts}


@register.filter
def get_tag_description(semantic_tags_json, tag):
    try:
        semantic_tags = json.loads(semantic_tags_json)
        return semantic_tags.get(tag, "")
    except json.JSONDecodeError:
        return ""
