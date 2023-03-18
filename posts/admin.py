from django.contrib import admin

from .models import Comment, Post


class PostAdmin(admin.ModelAdmin):
    list_display = [
        "author",
        "title",
        "link",
        "tags",
        "labels",
        "text",
        "created_date",
        "status",
    ]
    list_filter = ["status", "created_date", "author"]
    search_fields = ["title", "text", "tags", "labels"]
    raw_id_fields = ["author"]
    date_hierarchy = "created_date"
    ordering = ["status", "publish"]


class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "post", "created_date", "approved_comment")
    list_filter = ("created_date", "post")
    search_fields = ("author", "post", "text")


admin.site.register(Post)
admin.site.register(Comment)
