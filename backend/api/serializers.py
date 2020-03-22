from datastore.models import Symptom, Report

from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers


class SymptomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptom
        fields = "__all__"


class ReportSerializer(serializers.ModelSerializer):
    symptoms = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Symptom.objects.all(), required=True, allow_empty=False
    )

    class Meta:
        model = Report
        fields = "__all__"

    def validate_zip_code(self, value):
        if len(str(value)) != 5:
            raise serializers.ValidationError(_("ZIP Code must to be 5 chars long"))
        return value
