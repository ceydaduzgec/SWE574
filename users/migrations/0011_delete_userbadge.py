# Generated by Django 3.2.18 on 2023-03-26 21:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_badge_task_name'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserBadge',
        ),
    ]
