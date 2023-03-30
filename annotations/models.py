from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Annotation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='annotations')
    url = models.URLField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
