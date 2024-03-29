from django.urls import path

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Delivery Documentation",
        default_version="v1",
        description="Test description",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path(
        "docs/swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="swagger",
    ),
    path(
        "docs/redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]
