from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from taggit.models import Tag

from posts.models import Post, Space
from users.models import Contact

from .forms import CommentForm, EmailPostForm, PostForm, SpaceCreationForm, SpaceForm

User = get_user_model()


def check_link(request):
    link = request.GET.get("link", None)
    exists = Post.objects.filter(link=link).exists()
    return JsonResponse({"exists": exists})


@login_required
def create_space(request):
    if request.method == "POST":
        form = SpaceCreationForm(request.POST)
        if form.is_valid():
            space = form.save(commit=False)
            space.owner = request.user
            space.save()
            form.save_m2m()
            return redirect("space_detail", pk=space.pk)
    else:
        form = SpaceCreationForm()
    return render(request, "create_space.html", {"form": form})


@login_required
def space_list(request):
    spaces = Space.objects.all()
    return render(request, "space_list.html", {"spaces": spaces})


def space_detail(request, pk):
    space = get_object_or_404(Space, pk=pk)
    posts = space.posts.all()
    context = {"space": space, "posts": posts}
    return render(request, "space_detail.html", context)


@login_required
def post_list(request, tag_slug=None):
    # Getting friends of users
    friendsofUser = Contact.objects.filter(user_from=request.user).all()

    # Mapping friends of users
    friendsofUser = map(lambda x: x.user_to, friendsofUser)

    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by("-published_date")

    # filtering posts
    posts = (
        posts.filter(Q(author__in=friendsofUser) | Q(author=request.user))
        .annotate(total_comments=Count("comments"))
        .order_by("-published_date")
    )

    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])

    return render(request, "posts/post_list.html", {"posts": posts, "tag": tag})


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments

    stuff = get_object_or_404(Post, id=pk)
    total_likes = stuff.total_likes()
    post_tags_ids = post.tags.values_list("id", flat=True)
    similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by("-same_tags", "-published_date")[:10]

    return render(
        request,
        "posts/post_detail.html",
        {
            "post": post,
            "comments": comments,
            "similar_posts": similar_posts,
            "total_likes": total_likes,
        },
    )


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            post.tags.add(*form.cleaned_data["tags"])

            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm()
    return render(request, "posts/post_edit.html", {"form": form})


@login_required
def space_new(request):
    if request.method == "POST":
        form = SpaceForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            post.tags.add(*form.cleaned_data["tags"])

            return redirect("post_detail", pk=post.pk)
    else:
        form = SpaceForm()
    return render(request, "posts/post_edit.html", {"form": form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, "posts/post_edit.html", {"form": form})


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect("post_list")


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
    # List of similar posts

    return render(request, "posts/add_comment_to_post.html", {"form": form})


def search(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        searched = searched.lower()

        # Search posts
        posts_s = Post.objects.filter(
            Q(title__icontains=searched) | Q(text__icontains=searched) | Q(tags__name__icontains=searched)
        ).distinct()

        # Search spaces
        spaces_s = Space.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))

        return render(
            request,
            "posts/search.html",
            {
                "searched": searched,
                "posts_s": posts_s,
                "spaces_s": spaces_s,
            },
        )
    else:
        return render(request, "posts/search.html", {})


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
        "posts/my_research.html",
        {
            "posts": posts,
            "most_recent_posts": most_recent_posts,
            "most_commented_posts": most_commented_posts,
        },
    )


def faq(request):
    return render(request, "posts/faq.html")


def macro_economy(request):
    posts = Post.objects.filter(labels__contains="Macro")
    return render(request, "posts/my_research.html", {"posts": posts})


def equity(request):
    posts = Post.objects.filter(labels__contains="Equity")
    return render(request, "posts/my_research.html", {"posts": posts})


def fixed_income(request):
    posts = Post.objects.filter(labels__contains="Fixed")
    return render(request, "posts/my_research.html", {"posts": posts})


def company_news(request):
    posts = Post.objects.filter(labels__contains="company")
    return render(request, "posts/my_research.html", {"posts": posts})


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
    return render(request, "posts/share.html", {"post": post, "form": form, "sent": sent})


def like_post(request, pk):
    user_id = request.user.id
    post = get_object_or_404(Post, id=pk)
    if user_id:
        if post.likes.filter(id=user_id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        return JsonResponse({"status": "ok", "likes_count": post.total_likes()})
    return JsonResponse({"status": "error"})
