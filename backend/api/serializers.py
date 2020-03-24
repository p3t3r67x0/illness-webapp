from datastore.models import Symptom

from django.db import transaction
from rest_framework import serializers
from datastore.models import ZIPCode, Report


class SymptomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptom
        fields = "__all__"


class ReportSerializer(serializers.Serializer):
    zip_code = serializers.CharField(min_length=5, max_length=5)
    symptoms = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Symptom.objects.all(), required=True, allow_empty=False
    )

    class Meta:
        model = Report
        fields = ["zip_code", "symptoms"]

    @transaction.atomic()
    def create(self, validated_data):
        zip_code, _ = ZIPCode.objects.get_or_create(zip_code=validated_data["zip_code"])
        report = Report(
            zip_code=zip_code
        )
        report.save()
        report.symptoms.set(validated_data["symptoms"])
        return report
