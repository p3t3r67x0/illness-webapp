from datetime import datetime

from django.http import JsonResponse
from django.utils.translation import ugettext_lazy as _
from rest_framework import viewsets
from django.db.models import F, Count
from rest_framework.exceptions import ValidationError

from datastore.models import Symptom, Report

from .serializers import SymptomSerializer, ReportSerializer


class SymptomViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Symptom.objects.all().order_by("name")
    serializer_class = SymptomSerializer


class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer


class ReportResultViewSet(viewsets.ViewSet):
    def retrieve(self, request):
        qs_filter = {}

        zip_code_filter = request.GET.get("zip_code")
        if zip_code_filter:
            qs_filter["zip_code__zip_code"] = zip_code_filter

        county_filter = request.GET.get("county")
        if county_filter:
            qs_filter["zip_code__county__name"] = county_filter

        date_filter = request.GET.get("date")
        if date_filter:
            try:
                date_filter = datetime.strptime(date_filter, "%Y-%m-%d")
                qs_filter["created__date"] = date_filter
            except ValueError:
                raise ValidationError(_(f"Invalid date filter '{date_filter}'"))

        if "new_format" in request.GET:
            results = (
                Report.objects.filter(**qs_filter).values(
                    "zip_code__county__name",
                    "zip_code__county__longitude",
                    "zip_code__county__latitude",
                    "symptoms__name",
                )
                .annotate(users_count_affected=Count("id"))
                .annotate(symptom=F("symptoms__name"))
                .annotate(
                    county=F("zip_code__county__name"),
                    longitude=F("zip_code__county__longitude"),
                    latitude=F("zip_code__county__latitude"),
                )
                .values(
                    "county",
                    "longitude",
                    "latitude",
                    "users_count_affected",
                    "symptom",
                )
            )
            return JsonResponse(list(results), safe=False)
        else:
            results = (
                Report.objects.filter(**qs_filter).values("zip_code", "symptoms__name")
                .annotate(users_count_affected=Count("id"))
                .annotate(symptom=F("symptoms__name"))
                .values("zip_code__zip_code", "users_count_affected", "symptom")
                .annotate(zip_code=F("zip_code__zip_code"))
            )
            return JsonResponse(list(results), safe=False)
