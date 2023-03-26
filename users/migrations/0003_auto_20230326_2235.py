# Generated by Django 3.2.18 on 2023-03-26 19:35

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20230312_1832'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.AddField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(blank=True, max_length=150, verbose_name='Name'),
        ),
        migrations.AddField(
            model_name='user',
            name='photo',
            field=models.ImageField(blank=True, default='blank-profile-photo.jpeg', null=True, upload_to='users/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='follower_users', to=settings.AUTH_USER_MODEL, verbose_name='Followers'),
        ),
        migrations.DeleteModel(
            name='Contact',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
