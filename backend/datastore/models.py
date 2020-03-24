import requests

from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel
from rest_framework.exceptions import ValidationError


class Symptom(models.Model):
    name = models.CharField(
        _("Name"), max_length=255, blank=False, null=False, unique=True
    )


class County(models.Model):
    name = models.CharField(_("County"), max_length=255, blank=False, null=False)
    longitude = models.FloatField(_("Long geo coord"), blank=False, null=False)
    latitude = models.FloatField(_("Lat geo coord"), blank=False, null=False)

    def save(self, *args, **kwargs):
        if self.latitude is None or self.longitude is None:
            geo_coding_response = requests.get(
                "https://nominatim.openstreetmap.org/search",
                params={"country": "DE", "q": self.name, "format": "json",},
            )

            geo_coding_response.raise_for_status()
            geo_coding_response = geo_coding_response.json()
            if not len(geo_coding_response):
                raise ValidationError(
                    _(f"No geocoding info for county={self.name} found")
                )

            position = geo_coding_response[0]
            self.latitude = position["lat"]
            self.longitude = position["lon"]
        super().save(*args, **kwargs)


class ZIPCode(models.Model):
    zip_code = models.PositiveIntegerField(
        _("Zip code"), blank=False, null=False, unique=True
    )
    county = models.ForeignKey(
        County, blank=False, null=False, on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.zip_code)

    @transaction.atomic()
    def save(self, *args, **kwargs):
        try:
            self.county
        except County.DoesNotExist:
            geo_coding_response = requests.get(
                "https://nominatim.openstreetmap.org/search",
                params={
                    "country": "DE",
                    "postalcode": self.zip_code,
                    "addressdetails": 1,
                    "format": "json",
                },
            )

            geo_coding_response.raise_for_status()
            geo_coding_response = geo_coding_response.json()
            geo_coding_response = [
                c for c in geo_coding_response if c.get("osm_type") != "relation"
            ]
            if not len(geo_coding_response):
                raise ValidationError(
                    _(f"No geocoding info for zip={self.zip_code} found")
                )

            geo_coding_response = geo_coding_response[0]
            print(geo_coding_response)
            county = (
                geo_coding_response["address"].get("county")
                or f"{geo_coding_response['address'].get('city', geo_coding_response['address'].get('state'))} {geo_coding_response['address']['city_district']}"
            )
            self.county, created = County.objects.get_or_create(name=county)
        super().save(*args, **kwargs)


class Report(TimeStampedModel):
    zip_code = models.ForeignKey(
        ZIPCode, blank=False, null=True, on_delete=models.CASCADE
    )
    symptoms = models.ManyToManyField(Symptom, blank=False)

    @transaction.atomic()
    def save(self, *args, **kwargs):
        if self.zip_code is None:
            try:
                self.zip_code = ZIPCode.objects.get(zip_code=self.zip_code)
            except ZIPCode.DoesNotExist:
                self.zip_code = ZIPCode(zip_code=self.zip_code)
                self.zip_code.save()
        super().save(*args, **kwargs)
