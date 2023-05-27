from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Badge, UserBadge

User = get_user_model()


class FollowerInline(admin.TabularInline):
    model = User.followers.through
    fk_name = "to_user"
    verbose_name = "Follower"
    verbose_name_plural = "Followers"


class UserAdmin(BaseUserAdmin):
    list_display = ("username", "is_active", "is_staff", "is_superuser")
    list_filter = ("is_active", "is_staff", "is_superuser")
    search_fields = ("username", "first_name", "last_name", "photo", "bio", "email")
    inlines = (FollowerInline,)
    fieldsets = (
        (
            "Base Informations",
            {
                "fields": ("email", "password"),
            },
        ),
        (
            "Personal Informations",
            {
                "fields": (
                    "username",
                    "first_name",
                    "last_name",
                    "photo",
                )
            },
        ),
        ("General Informations", {"fields": ("last_login", "date_joined")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Activities",
            {
                "fields": (
                    "following",
                    "bookmarks",
                    "followers",
                )
            },
        ),
    )
    readonly_fields = ("last_login", "date_joined", "followers")
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "first_name", "last_name", "password1", "password2"),
            },
        ),
    )

    def followers(self, instance):
        if instance.followers.count() != 0:
            followers = instance.followers.all()
            return followers

    followers.short_description = "Followers"


admin.site.register(User, UserAdmin)


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "image")


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ("user", "badge", "date")
