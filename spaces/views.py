from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from spaces.models import Space
from spaces.forms import SpaceCreationForm, SpaceForm

User = get_user_model()


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
