from django.db import models

# Create your models here.


class Tag(models.Model):
    wikidata_id = models.CharField(max_length=15, unique=True)
    label = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.label
