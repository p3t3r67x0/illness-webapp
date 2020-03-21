from datastore.models import Symptom
from rest_framework import serializers


class SymptomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptom
        fields = "__all__"
