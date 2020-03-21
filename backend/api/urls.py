from django.urls import path

from .views import SymptomViewSet, ReportViewSet

app_name = "api"

urlpatterns = [
    path(r"symptom/", SymptomViewSet.as_view({"get": "list"}), name="symptom"),
    path(r"report/", ReportViewSet.as_view({"post": "create"}), name="report"),
]
