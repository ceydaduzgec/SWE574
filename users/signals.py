from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
from posts.models import Comment, Post
from spaces.models import Space


@receiver(post_save, sender=Comment)
def award_comment_badge(sender, instance, created, **kwargs):
    if created:
        user = instance.author
        comments_count = Comment.objects.filter(author=user).count()

        if comments_count >= 1:
            badge = Badge.objects.get(name='Comment Duck')
            user_badge, created = UserBadge.objects.get_or_create(user=user, badge=badge)
            if created:
                " send notification to user "
                user_badge.save()
                pass
        if comments_count >= 5:
            badge = Badge.objects.get(name='Comment Knight')
            user_badge, created = UserBadge.objects.get_or_create(user=user, badge=badge)
            if created:
                " send notification to user "
                user_badge.save()
                pass

            if comments_count >= 10:
                badge = Badge.objects.get(name='Comment King')
                user_badge, created = UserBadge.objects.get_or_create(user=user, badge=badge)
                if created:
                    " send notification to user "
                    user_badge.save()
                    pass

@receiver(post_save, sender=Space)
def award_space_badge(sender, instance, created, **kwargs):
    if created:
        user = instance.owner
        space_count = Space.objects.filter(owner=user).count()

        if space_count >= 1:
            badge = Badge.objects.get(name='Space Duck')
            user_badge, created = UserBadge.objects.get_or_create(user=user, badge=badge)
            if created:
                " send notification to user "
                user_badge.save()
                pass
        if space_count >= 2:
            badge = Badge.objects.get(name='Space Knight')
            user_badge, created = UserBadge.objects.get_or_create(user=user, badge=badge)
            if created:
                " send notification to user "
                user_badge.save()
                pass

        if space_count >= 3:
            badge = Badge.objects.get(name='Space King')
            user_badge, created = UserBadge.objects.get_or_create(user=user, badge=badge)
            if created:
                " send notification to user "
                user_badge.save()
                pass

@receiver(post_save, sender=Post)
def award_post_badge(sender, instance, created, **kwargs):
    if created:
        user = instance.author
        post_count = Post.objects.filter(author=user).count()

        if post_count >= 1:
            badge = Badge.objects.get(name='Post Duck')
            user_badge, created = UserBadge.objects.get_or_create(user=user, badge=badge)
            if created:
                " send notification to user "
                user_badge.save()
                pass
        if post_count >= 2:
            badge = Badge.objects.get(name='Post Knight')
            user_badge, created = UserBadge.objects.get_or_create(user=user, badge=badge)
            if created:
                " send notification to user "
                user_badge.save()
                pass

            if post_count >= 3:
                badge = Badge.objects.get(name='Post King')
                user_badge, created = UserBadge.objects.get_or_create(user=user, badge=badge)
                if created:
                    " send notification to user "
                    user_badge.save()
                    pass
