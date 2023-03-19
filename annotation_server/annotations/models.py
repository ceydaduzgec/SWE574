from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _


class URI(models.Model):
    id = models.URLField(primary_key=True)
    format = models.CharField(max_length=100)
    language = models.JSONField()
    textDirection = models.CharField(max_length=10)
    processingLanguage = models.CharField(max_length=100)

    def __str__(self):
        return str(self.id)


class Annotation(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    type = models.CharField(max_length=255)
    motivation = models.CharField(max_length=255)
    body = JSONField()
    target = models.ManyToManyField(URI, verbose_name=_("uris"))
    selector = JSONField(null=True)

    class Meta:
        ordering = ["created_at"]
        verbose_name = "annotation"
        verbose_name_plural = "annotations"

    def as_dict(self):
        annotation_dict = {
            "@context": "http://www.w3.org/ns/anno.jsonld",
            "id": self.id,
            "type": self.type,
            "motivation": self.motivation,
            "body": self.body,
            "target": self.target,
        }
        if self.selector:
            annotation_dict["selector"] = self.selector
        return annotation_dict
