from django.urls import path

from .views import SymptomViewSet, ReportViewSet, ReportResultViewSet

app_name = "api"

urlpatterns = [
    path(r"symptom/", SymptomViewSet.as_view({"get": "list"}), name="symptom"),
    path(r"report/", ReportViewSet.as_view({"post": "create"}), name="report"),
    path(r"report/result/", ReportResultViewSet.as_view({"get": "retrieve"}), name="report_result"),
]
