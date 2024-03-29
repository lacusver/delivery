"""
URL configuration for delivery project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from .yasg import urlpatterns as docs_url
from apps.service_delivery.views import CargoViewSet, CarViewSet


def get_router_for_version_one():
    router = DefaultRouter()
    router.register("cargo", CargoViewSet, basename="cargo")
    router.register("car", CarViewSet, basename="car")
    return router


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/v1/",
        include(
            (get_router_for_version_one().get_urls(), "main"), namespace="v1"
        ),
    ),
]

urlpatterns += docs_url
if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
