from django.http import JsonResponse
from rest_framework import viewsets
from django.db.models import F, Count
from datastore.models import Symptom, Report

from .serializers import SymptomSerializer, ReportSerializer


class SymptomViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Symptom.objects.all().order_by("name")
    serializer_class = SymptomSerializer


class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer


class ReportResultViewSet(viewsets.ViewSet):
    def retrieve(self, request):
        if "new_format" in request.GET:
            results = (
                Report.objects.values(
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
                Report.objects.values("zip_code", "symptoms__name")
                .annotate(users_count_affected=Count("id"))
                .annotate(symptom=F("symptoms__name"))
                .values("zip_code__zip_code", "users_count_affected", "symptom")
                .annotate(zip_code=F("zip_code__zip_code"))
            )
            return JsonResponse(list(results), safe=False)
