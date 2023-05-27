from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Count, Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from posts.forms import CommentForm, EmailPostForm, PostForm
from posts.models import Post, TagDescription
from spaces.models import Space
from taggit.models import Tag

User = get_user_model()


def check_link(request):
    link = request.GET.get("link", None)
    exists = Post.objects.filter(link=link).exists()
    return JsonResponse({"exists": exists})


@login_required
def post_list(request, tag_slug=None):
    user = request.user
    spaces = Space.objects.filter(Q(owner=user) | Q(members=user) | Q(granted_members=user) | Q(moderators=user))
    posts = (
        Post.objects.filter(Q(spaces__in=spaces) | Q(author__in=user.following.all()) | Q(author=user))
        .annotate(total_comments=Count("comments"))
        .order_by("-published_date")
    )

    context = {"posts": posts}

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
        context["tag"] = tag

    return render(request, "post_list.html", context)


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()

    # Get the moderators of the spaces of the post
    moderators = []
    for space in post.spaces.all():
        for moderator in space.moderators.all():
            moderators.append(moderator)

    stuff = get_object_or_404(Post, id=pk)
    total_likes = stuff.total_likes()
    post_tags_ids = post.tags.values_list("id", flat=True)
    similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by("-same_tags", "-published_date")[:10]

    return render(
        request,
        "post_detail.html",
        {
            "post": post,
            "comments": comments,
            "similar_posts": similar_posts,
            "total_likes": total_likes,
            "moderators": moderators,
        },
    )


@login_required
def post_new(request):
    space_pk = request.GET.get("space_pk")
    if space_pk:
        space = get_object_or_404(Space, pk=space_pk)
    else:
        space = None

    duplicatespaces = (
        request.user.owned_spaces.all()
        | request.user.moderated_spaces.all()
        | Space.objects.filter(posting_permission="all", members=request.user)
        | Space.objects.filter(posting_permission="granted", granted_members=request.user)
    )
    spaces = duplicatespaces.values("id", "name").distinct()

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, selected_space=space, user=request.user)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()

            # Check if an image was uploaded
            if "image" not in request.FILES:
                post.image = "none.jpg"

            post.save()

            # Get the selected spaces from the form and add them to the post
            selected_spaces = form.cleaned_data.get("spaces")
            if selected_spaces:
                post.spaces.set(selected_spaces)

            post.tags.add(*form.cleaned_data["tags"])

            tag_descriptions_data = request.POST.getlist("tag_descriptions[]")

            for tag_description_data in tag_descriptions_data:
                tag_name, description = tag_description_data.split(":", 1)
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                tag_description, _ = TagDescription.objects.get_or_create(tag=tag, description=description)
                post.tag_descriptions.add(tag_description)

            # Save the post instance with the new tag descriptions
            post.save()

            return redirect("post_detail", pk=post.pk)
    else:
        initial_data = {}
        if space:
            initial_data["spaces"] = [space.pk]
        form = PostForm(initial=initial_data, selected_space=space, user=request.user)

    return render(request, "post_edit.html", {"form": form, "spaces": spaces})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()

            # heck if an image was uploaded
            if "image" not in request.FILES:
                post.image = None

            post.tags.clear()  # clear existing tags
            tags = form.cleaned_data["tags"]
            if isinstance(tags, list):
                tags = ",".join(tags)
            tags_list = [tag.strip() for tag in tags.split(",")]
            for tag in tags_list:
                if tag:
                    t, created = Tag.objects.get_or_create(name=tag)
                    post.tags.add(t)
            post.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, "post_editor.html", {"form": form, "post": post})


@require_POST
@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.author:
        post.delete()
    else:
        for space in post.spaces.all():
            if request.user in space.moderators.all():
                space.posts.remove(post)
        post.save()
    return redirect("post_list")


@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = CommentForm()

    return render(request, "add_comment_to_post.html", {"form": form})


def search(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        searched = searched.lower()

        # Search posts with the given keyword
        posts_s = Post.objects.filter(
            Q(title__icontains=searched)
            | Q(text__icontains=searched)
            | Q(tags__name__icontains=searched)
            | Q(tag_descriptions__description__icontains=searched)
        ).distinct()

        # Search spaces with the given keyword
        spaces_s = Space.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))

        return render(
            request,
            "search.html",
            {
                "searched": searched,
                "posts_s": posts_s,
                "spaces_s": spaces_s,
            },
        )
    else:
        return render(request, "search.html", {})


def my_research(request):
    posts = Post.objects.filter(author_id=request.user.id).order_by("-published_date")

    most_recent_posts = Post.objects.filter(author_id=request.user.id).order_by("-published_date")[:3]

    most_commented_posts = (
        Post.objects.filter(author_id=request.user.id)
        .annotate(total_comments=Count("comments"))
        .order_by("-total_comments")[:3]
    )

    return render(
        request,
        "my_research.html",
        {
            "posts": posts,
            "most_recent_posts": most_recent_posts,
            "most_commented_posts": most_commented_posts,
        },
    )


@require_POST
@login_required
def post_share(request, pk):
    # Retrieve post by id
    post = get_object_or_404(Post, id=pk)
    sent = False
    if request.method == "POST":
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{post.author} recommends you read {post.title} "

            message = f"Read {post.title} at {post_url}\n\n"

            send_mail(subject, message, "swebogazici@gmail.com", [cd["to"]])
            sent = True
    else:
        form = EmailPostForm()

    return render(request, "share.html", {"post": post, "form": form, "sent": sent})


@require_POST
@login_required
def toggle_like(request, pk):
    user_id = request.user.id
    post = get_object_or_404(Post, id=pk)
    if user_id:
        if post.likes.filter(id=user_id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@require_POST
@login_required
def toggle_bookmark(request, pk):
    post = get_object_or_404(Post, id=pk)
    user = request.user

    if post in user.bookmarks.all():
        user.bookmarks.remove(post)
    else:
        user.bookmarks.add(post)

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
