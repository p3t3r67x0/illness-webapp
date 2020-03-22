from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel


class Symptom(models.Model):
    name = models.CharField(
        _("Name"), max_length=255, blank=False, null=False, unique=True
    )


class Report(TimeStampedModel):
    zip_code = models.PositiveIntegerField(_("Zip code"), blank=False, null=False)
    symptoms = models.ManyToManyField(Symptom, blank=False)
