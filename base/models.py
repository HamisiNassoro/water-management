from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres import fields as postgres_fields

class Index(models.Model):
    id = models.AutoField(primary_key=True)
    submission = models.PositiveSmallIntegerField(default=1)

    class Meta:
        verbose_name = _("Index")
        verbose_name_plural = _("Indices")

    @property
    def next_submission(self):
        self.submission += 1
        self.save()
        return self.submission

    def __str__(self):
        return f"{self.id}"

