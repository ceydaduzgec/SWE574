from django.db.models.signals import post_save
from django.dispatch import receiver

from posts.models import Comment, Post
from spaces.models import Space

from .models import *


@receiver(post_save, sender=Comment)
def award_comment_badge(sender, instance, created, **kwargs):
    if created:
        user = instance.author
        comments_count = Comment.objects.filter(author=user).count()

        if comments_count >= 1:
            badge, created = Badge.objects.get_or_create(
                name="Commentator",
                defaults={"description": "Awarded for creating your first comment.", "image": "badges/commentator.png"},
            )
            user_badge, created = UserBadge.objects.get_or_create(user=user, badge=badge)
            if created:
                "send notification to user"
                user_badge.save()

        if comments_count >= 2:
            badge, created = Badge.objects.get_or_create(
                name="Chatty Cathy",
                defaults={
                    "description": "Awarded for creating 2 or more comments.",
                    "image": "badges/chatty-cathy.png",
                },
            )
            user_badge, created = UserBadge.objects.get_or_create(user=user, badge=badge)
            if created:
                "send notification to user"
                user_badge.save()

        if comments_count >= 3:
            badge, created = Badge.objects.get_or_create(
                name="Comment King",
                defaults={
                    "description": "Awarded for creating 3 or more comments.",
                    "image": "badges/comment-king.png",
                },
            )
            user_badge, created = UserBadge.objects.get_or_create(user=user, badge=badge)
            if created:
                "send notification to user"
                user_badge.save()


@receiver(post_save, sender=Space)
def award_space_badge(sender, instance, created, **kwargs):
    if created:
        user = instance.owner
        space_count = Space.objects.filter(owner=user).count()

        if space_count >= 1:
            badge, created = Badge.objects.get_or_create(
                name="Explorer",
                defaults={"description": "Awarded for creating your first space.", "image": "badges/explorer.png"},
            )
            user_badge, created = UserBadge.objects.get_or_create(user=user, badge=badge)
            if created:
                "send notification to user"
                user_badge.save()

        if space_count >= 2:
            badge, created = Badge.objects.get_or_create(
                name="Organizer",
                defaults={"description": "Awarded for creating 2 or more spaces.", "image": "badges/organizer.png"},
            )
            user_badge, created = UserBadge.objects.get_or_create(user=user, badge=badge)
            if created:
                "send notification to user"
                user_badge.save()

        if space_count >= 3:
            badge, created = Badge.objects.get_or_create(
                name="Space Star",
                defaults={"description": "Awarded for creating 3 or more spaces.", "image": "badges/space-star.png"},
            )
            user_badge, created = UserBadge.objects.get_or_create(user=user, badge=badge)
            if created:
                "send notification to user"
                user_badge.save()


@receiver(post_save, sender=Post)
def award_post_badge(sender, instance, created, **kwargs):
    if created:
        user = instance.author
        post_count = Post.objects.filter(author=user).count()

        if post_count >= 1:
            badge, created = Badge.objects.get_or_create(
                name="Post Duck",
                defaults={"description": "Awarded for creating your first post.", "image": "badges/post-duck.png"},
            )
            user_badge, created = UserBadge.objects.get_or_create(user=user, badge=badge)
            if created:
                "send notification to user"
                user_badge.save()

        if post_count >= 2:
            badge, created = Badge.objects.get_or_create(
                name="Prolific Poster",
                defaults={
                    "description": "Awarded for creating 2 or more posts.",
                    "image": "badges/prolific-poster.png",
                },
            )
            user_badge, created = UserBadge.objects.get_or_create(user=user, badge=badge)
            if created:
                "send notification to user"
                user_badge.save()

        if post_count >= 3:
            badge, created = Badge.objects.get_or_create(
                name="Post King",
                defaults={"description": "Awarded for creating 3 or more posts.", "image": "badges/post-king.png"},
            )
            user_badge, created = UserBadge.objects.get_or_create(user=user, badge=badge)
            if created:
                "send notification to user"
                user_badge.save()
