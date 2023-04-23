from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import auth
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from posts.models import Post
from users.forms import NewUserForm, UserEditForm

User = get_user_model()


def login_request(request):
    if request.user.is_authenticated:
        return redirect("post_list")
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
                return redirect("post_list")
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
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password1"],
            )
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("post_list")
        else:
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
            "userToSee": user,
            "id": user.id,
            "latest_posts_db": all_posts[:4],
            "count": all_posts.count(),
            "most_commented_posts": most_commented_posts,
        },
    )


@require_POST
@login_required
def user_follow(request, username):
    current_user = request.user
    if username != current_user.username:
        try:
            user_to_follow = get_object_or_404(User, username=username)
            if current_user.following.filter(id=user_to_follow.id).exists():
                current_user.following.remove(user_to_follow)
            else:
                current_user.following.add(user_to_follow)
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

        except User.DoesNotExist:
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request, "user_list.html", {"section": "people", "users": users})


@login_required
def my_account(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        if user_form.is_valid():
            user_form.save()

    else:
        user_form = UserEditForm(instance=request.user)
    return render(
        request,
        "my_account.html",
        {"user_form": user_form},
    )
