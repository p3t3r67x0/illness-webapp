from datetime import datetime

from django.http import JsonResponse
from django.utils.translation import ugettext_lazy as _
from rest_framework import viewsets
from django.db.models import F, Count
from django.db.models.functions import TruncDate
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
            qs_filter["zip_code__county__name__iexact"] = county_filter

        date_filter = request.GET.get("date")
        if date_filter:
            try:
                date_filter = datetime.strptime(date_filter, "%Y-%m-%d")
                qs_filter["created__date"] = date_filter
            except ValueError:
                raise ValidationError(_(f"Invalid date filter '{date_filter}'"))

        results = (
            Report.objects.filter(**qs_filter)
            .values(
                "zip_code__county__name",
                "symptoms__name",
                "created__date",
                "zip_code__county__longitude",
                "zip_code__county__latitude",
            )
            .annotate(
                county=F("zip_code__county__name"),
                date=TruncDate("created__date"),
                symptom=F("symptoms__name"),
                longitude=F("zip_code__county__longitude"),
                latitude=F("zip_code__county__latitude"),
            )
            .annotate(users_count_affected=Count("id"))
            .values(
                "county",
                "date",
                "symptom",
                "longitude",
                "latitude",
                "users_count_affected",
            )
        )

        return JsonResponse(list(results), safe=False)
