from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import User,Badge, UserBadge


User = get_user_model()

admin.site.register(User)

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "image")

@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ("user", "badge", "date")