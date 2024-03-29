from django.db.models import QuerySet
from apps.service_delivery.models import Cargo, Car
from .dto import CargoListDTO, CarListDTO, CargoDistancesDTO
from geopy import distance


def get_nearby_cars_amount_for_cargos(
    cargo_queryset: QuerySet[Cargo], distance=450
):
    car_queryset: QuerySet[Car] = Car.geo_objects.all()
    cargo_list = []
    for cargo in cargo_queryset:
        car_amount = car_queryset.near(
            cargo.pick_up_location.geo_lat,
            cargo.pick_up_location.geo_lon,
            distance,
        ).count()
        cargo_list.append(CargoListDTO(cargo, car_amount))
    return cargo_list


def get_cars_for_cargos(cargo: Cargo):
    car_queryset: QuerySet[Car] = Car.objects.all()
    car_locations = []
    for car in car_queryset:
        if car.location.geo_lat and car.location.geo_lon:
            exact_distance = distance.distance(
                (
                    cargo.pick_up_location.geo_lat,
                    cargo.pick_up_location.geo_lon,
                ),
                (car.location.geo_lat, car.location.geo_lon),
            ).miles
            car_locations.append(CarListDTO(car, exact_distance))

    return CargoDistancesDTO(cargo, car_locations)
