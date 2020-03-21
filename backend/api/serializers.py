from datastore.models import Symptom, Report
from rest_framework import serializers


class SymptomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptom
        fields = "__all__"


class ReportSerializer(serializers.ModelSerializer):
    symptoms = serializers.PrimaryKeyRelatedField(many=True, queryset=Symptom.objects.all(), required=True)

    class Meta:
        model = Report
        fields = "__all__"
