from django.urls import path

from posts.views import (
    add_comment_to_post,
    check_link,
    like_post,
    my_research,
    post_detail,
    post_edit,
    post_list,
    post_new,
    post_remove,
    post_share,
    search,
)

urlpatterns = [
    path("home", post_list, name="post_list"),
    path("<int:labels>/", post_list, name="post_list"),
    path("post/new/", post_new, name="post_new"),
    path("post/<int:pk>/share/", post_share, name="post_share"),
    path("post/<int:pk>/editor/", post_edit, name="post_edit"),
    path("post/<int:pk>/remove/", post_remove, name="post_remove"),
    path("post/<int:pk>/", post_detail, name="post_detail"),
    path("post/<int:pk>/comment/", add_comment_to_post, name="add_comment_to_post"),
    path("post/search/", search, name="search"),
    path("myresearch/", my_research, name="my_research"),  # TODO: what is the difference between search
    path("tag/<slug:tag_slug>/", post_list, name="post_list_by_tag"),
    path("like/<int:pk>", like_post, name="like_post"),
    path("check_link/", check_link, name="check_link"),
    path("", post_list, name="post_list_"),
]
