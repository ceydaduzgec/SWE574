from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import auth
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from posts.models import Post
from users.forms import NewUserForm, ProfileEditForm, UserEditForm
from users.models import Contact, Profile
from .models import Badge, BadgeTasks, Contact, Profile

User = get_user_model()


def login_request(request):
    if request.user.is_authenticated:
        return redirect("/home")
    """ REDIRECT IF USER ALREADY LOGGED IN """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are logged in as {username}. Welcome!")
                return redirect("/home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(
        request=request,
        template_name="users/templates/login.html",
        context={"login_form": form},
    )


def register_request(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)

            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("/")
        else:
            messages.error(request, form.errors)
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(
        request=request,
        template_name="users/templates/register.html",
        context={"register_form": form},
    )


def logout_request(request):
    # if not request.user.is_authenticated:
    #     return redirect("/")
    #
    # logout(request)
    # messages.info(request, "Logged out successfully!"),
    auth.logout(request)
    return redirect("login")


def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully")
        else:
            messages.error(request, "Error updating your profile")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(
        request,
        "edit.html",
        {"user_form": user_form, "profile_form": profile_form},
        # "posts:my_account.html",
        # {"user_form": user_form, "profile_form": profile_form},  # TODO: which html should be used
        # "posts:my_account.html",
    )


@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)

    all_posts = Post.objects.filter(author=user.id)
    # most_commented_posts = Post.objects.filter(author_id=request.user.id).annotate(
    #     total_comments=Count('comments')).order_by('-total_comments')[:3]
    most_commented_posts = (
        Post.objects.filter(author_id=user.id)
        .annotate(total_comments=Count("comments"))
        .order_by("-total_comments")[:4]
    )

    return render(
        request,
        "user_detail.html",
        {
            "section": "people",
            "userToSee": user,
            "id": user.id,
            "latest_posts_db": all_posts[:4],
            "count": all_posts.count(),
            "most_commented_posts": most_commented_posts,
        },
    )


@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get("id")
    action = request.POST.get("action")
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == "follow":
                Contact.objects.get_or_create(user_from=request.user, user_to=user)

            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({"status": "ok"})
        except User.DoesNotExist:
            return JsonResponse({"status": "error"})
    return JsonResponse({"status": "error"})


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request, "user_list.html", {"section": "people", "users": users})


def my_account(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(
        request,
        "my_account.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


@login_required
def list_tasks(request):
    tasks = BadgeTasks.objects.filter(user=request.user)
    badges = Profile.objects.get(user=request.user).badges.all()
    return render(request, 'list_tasks.html', {'tasks': tasks, 'badges': badges})



def complete_task(request, task_id):
    task = get_object_or_404(BadgeTasks, id=task_id, user=request.user)

    if not task.completed:
        task.completed = True
        task.save()

        # Reward a badge if the task has an associated badge
        if task.badge:
            request.user.userprofile.badges.add(task.badge)

    return redirect('list_tasks')  # Replace 'tasks' with the name of the view that displays tasks
