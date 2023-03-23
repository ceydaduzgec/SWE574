from django.db import models

# Create your models here.

class WebAnnotation(models.Model):
    target = models.URLField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Annotation for {self.target}"