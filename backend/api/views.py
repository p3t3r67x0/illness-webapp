from django.http import JsonResponse
from rest_framework import viewsets, views
from django.db.models import F, Count
from datastore.models import Symptom, Report

from .serializers import SymptomSerializer, ReportSerializer


class SymptomViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Symptom.objects.all().order_by("name")
    serializer_class = SymptomSerializer


class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer


class ReportResultViewSet(viewsets.ViewSet):
    def retrieve(self, *args):
        results = (
            Report.objects.values("zip_code_shortened", "symptoms__name")
            .annotate(users_count_affected=Count("id"))
            .annotate(zip_code=F("zip_code_shortened"))
            .annotate(symptom=F("symptoms__name"))
            .values("zip_code", "users_count_affected", "symptom")
        )
        return JsonResponse(list(results), safe=False)
