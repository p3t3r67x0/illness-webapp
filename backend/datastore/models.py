from django.db import models
from django.utils.translation import ugettext_lazy as _


class Symptom(models.Model):
    name = models.CharField(_("Name"), max_length=255, blank=False, null=False, unique=True)
