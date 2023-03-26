from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from spaces.forms import SpaceCreationForm, SpaceForm
from spaces.models import Space

from .forms import SpacePolicyForm

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
    is_owner = request.user == space.owner
    context = {"space": space, "posts": posts, "is_owner": is_owner}
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
    return render(request, "post_edit.html", {"form": form})


@login_required
def space_policies(request, pk):
    space = get_object_or_404(Space, pk=pk)
    if not request.user == space.owner:
        raise Http404

    if request.method == "POST":
        form = SpacePolicyForm(request.POST, instance=space)
        if form.is_valid():
            form.save()
            messages.success(request, "Space policies updated successfully.")
            return redirect("space_detail", pk=pk)
    else:
        form = SpacePolicyForm(instance=space)
    return render(request, "spaces/templates/space_policies.html", {"space": space, "form": form})


@login_required
def my_spaces_list(request):
    spaces = Space.objects.filter(Q(owner=request.user) | Q(moderators=request.user)).distinct()
    context = {"spaces": spaces}
    return render(request, "my_spaces_list.html", context)
