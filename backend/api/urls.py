from django.urls import path

from .views import SymptomViewSet

app_name = "api"

urlpatterns = [
    path(r"symptom/", SymptomViewSet.as_view({"get": "list"}), name="symptoms"),
]
