import string

from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _

from .models import Index

from .utils import key_generator

class SUBField(models.CharField):
    description = _("Unique character string (up to %(max_length)s)")

    def __init__(self, prefix="", *args, **kwargs):
        self.prefix = prefix
        super(SUBField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        _value = getattr(model_instance, self.attname)
        if add and any([_value == "", not _value]):
            ind = Index.objects.first()
            code = "{:06d}".format(ind.next_submission)
            setattr(model_instance, self.attname, f"{self.prefix}{code}")
            return f"{self.prefix}{code}"
        else:
            return super(SUBField, self).pre_save(model_instance, add)