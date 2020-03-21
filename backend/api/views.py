from rest_framework import viewsets

from datastore.models import Symptom

from .serializers import SymptomSerializer, ReportSerializer


class SymptomViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Symptom.objects.all().order_by("name")
    serializer_class = SymptomSerializer


class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
