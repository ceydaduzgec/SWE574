from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.shortcuts import redirect
from spaces.forms import SpaceCreationForm
from spaces.models import Space

from .forms import SpacePolicyForm

User = get_user_model()

def join_space(request, pk):
    space = get_object_or_404(Space, pk=pk)
    space.members.add(request.user)
    return redirect("space_detail", pk=pk)

def leave_space(request, pk):
    space = get_object_or_404(Space, pk=pk)
    if request.user in space.members.all() or request.user in space.granted_members.all():
        space.members.remove(request.user)
        space.granted_members.remove(request.user)
    return redirect("space_detail", pk=pk)


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

# views.py
from django.shortcuts import render, get_object_or_404
from .models import Space

def space_members(request, pk):
    space = get_object_or_404(Space, pk=pk)
    moderators = space.moderators.all()
    members = space.members.all()
    granted_members = space.granted_members.all()
    combined_members = members | granted_members
    context = {
        "space": space,
        "moderators": moderators,
        "members": members,
        "granted_members": granted_members,
        "combined_members": combined_members,
    }
    return render(request, "spaces/templates/space_members.html", context)

@login_required
def my_spaces_list(request):
    spaces = Space.objects.filter(Q(owner=request.user) | Q(moderators=request.user)).distinct()
    context = {"spaces": spaces}
    return render(request, "my_spaces_list.html", context)
