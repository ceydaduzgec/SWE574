# Generated by Django 3.2.18 on 2023-03-23 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spaces', '0005_auto_20230321_2059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='space',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]