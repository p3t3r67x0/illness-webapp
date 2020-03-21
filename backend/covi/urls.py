from django.urls import include, path

urlpatterns = [path(r"api/v1/", include("api.urls"))]
