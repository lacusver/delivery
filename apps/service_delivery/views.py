from rest_framework import viewsets, filters, mixins
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Cargo, Car
from .serializers import (
    CargoSerializer,
    CargoListSerializer,
    CargoCreateSerializer,
    CarSerializer,
    CargoDetailSerializer,
)
from .service.geopy import (
    get_nearby_cars_amount_for_cargos,
    get_cars_for_cargos,
)
from utils.custom_exceptions import BadRequest
from rest_framework.exceptions import APIException
from django.conf import settings


class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargo.objects.all().select_related(
        "pick_up_location", "delivery_location"
    )
    serializer_class = CargoSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_fields = ("weight",)
    ordering_fields = ("weight",)
    # filterset_class = EventFilter

    def get_serializer_class(self):
        if self.action == "retrieve" and self.request.method == "GET":
            return CargoDetailSerializer
        if self.request.method == "POST":
            return CargoCreateSerializer
        return super().get_serializer_class()

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "distance",
                openapi.IN_QUERY,
                "Distance in miles",
                type=openapi.TYPE_NUMBER,
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        distance = settings.DISTANCE
        if request.query_params:
            try:
                distance_params = request.query_params.get("distance")
                if distance_params not in [None, ""]:
                    distance = float(distance_params)
            except ValueError:
                raise BadRequest(detail="Incorrect query params")
            except Exception:
                raise APIException(
                    detail="Something went wrong with query params, try again"
                )

        cargo_list = get_nearby_cars_amount_for_cargos(
            cargo_queryset=self.filter_queryset(self.queryset),
            distance=distance,
        )
        serializer = CargoListSerializer(cargo_list, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        cargo_cars = get_cars_for_cargos(instance)
        serializer = self.get_serializer(cargo_cars)
        return Response(serializer.data)


class CarViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Car.objects.all().select_related("location")
    serializer_class = CarSerializer
