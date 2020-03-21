from rest_framework import viewsets

from datastore.models import Symptom

from .serializers import SymptomSerializer


class SymptomViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Symptom.objects.all().order_by("name")
    serializer_class = SymptomSerializer

    search_fields = [
        "name",
    ]
