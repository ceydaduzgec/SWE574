from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from spaces.forms import SpaceCreationForm
from spaces.models import Space

from .forms import SpacePolicyForm

User = get_user_model()


@login_required
def delete_space(request, pk):
    space = get_object_or_404(Space, pk=pk)

    if not request.user == space.owner:
        return HttpResponseForbidden()

    if request.method == "POST":
        space.delete()
        return redirect("my_spaces_list")


def grant_permission(request, space_pk, member_pk):
    space = get_object_or_404(Space, pk=space_pk)
    member = get_object_or_404(User, pk=member_pk)
    if request.method == "POST":
        space.granted_members.add(member)
        space.members.remove(member)
    return redirect("space_members", pk=space.pk)


def ungrant_permission(request, space_pk, member_pk):
    space = get_object_or_404(Space, pk=space_pk)
    member = get_object_or_404(User, pk=member_pk)
    if request.method == "POST":
        space.granted_members.remove(member)
        space.members.add(member)
    return redirect("space_members", pk=space.pk)


@login_required
def remove_member(request, space_pk, member_pk):
    space = get_object_or_404(Space, pk=space_pk)
    member = get_object_or_404(User, pk=member_pk)
    if request.method == "POST":
        space.members.remove(member)
        space.granted_members.remove(member)
    return redirect("space_members", pk=space.pk)


@login_required
def make_moderator(request, space_pk, member_pk):
    space = get_object_or_404(Space, pk=space_pk)
    member = get_object_or_404(User, pk=member_pk)
    if request.method == "POST":
        space.moderators.add(member)
        space.members.remove(member)
        space.granted_members.remove(member)
    return redirect("space_members", pk=space.pk)


@login_required
def remove_moderator(request, space_pk, moderator_pk):
    space = get_object_or_404(Space, pk=space_pk)
    moderator = get_object_or_404(User, pk=moderator_pk)
    if request.method == "POST":
        space.moderators.remove(moderator)
    return redirect("space_members", pk=space.pk)


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
    can_post = space.can_member_post(request.user)  # check if the user can post on the space
    context = {"space": space, "posts": posts, "is_owner": is_owner, "can_post": can_post}
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
            return redirect("space_detail", pk=pk)
    else:
        form = SpacePolicyForm(instance=space)
    return render(request, "spaces/templates/space_policies.html", {"space": space, "form": form})


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
    spaces = Space.objects.filter(
        Q(owner=request.user) | Q(moderators=request.user) | Q(members=request.user) | Q(granted_members=request.user)
    ).distinct()

    recommended_spaces = (
        Space.objects.exclude(
            Q(owner=request.user)
            | Q(moderators=request.user)
            | Q(members=request.user)
            | Q(granted_members=request.user)
        )
        .annotate(posts_count=Count("posts"))
        .order_by("-posts_count")
        .exclude(pk__in=[space.pk for space in spaces])[:5]
    )

    context = {
        "spaces": spaces,
        "recommended_spaces": recommended_spaces,
    }

    return render(request, "my_spaces_list.html", context)


@login_required
def newspace(request):
    return render(request, "spaces/templates/spaces_initial.html")
