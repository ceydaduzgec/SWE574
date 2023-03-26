from django.contrib import admin

from .models import Contact, Profile, Badge, BadgeTasks


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "date_of_birth", "photo"]


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("user_from", "user_to", "created")

@admin.register(Badge)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "image")


@admin.register(BadgeTasks)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "completed", "user", "badge", "date_awarded")