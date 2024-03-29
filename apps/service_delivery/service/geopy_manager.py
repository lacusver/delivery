from django.db import models
from geopy import units, distance


class GeoQuerySet(models.QuerySet):
    def near(self, latitude=None, longitude=None, distance_range=450):
        queryset = self

        if not (latitude and longitude and distance_range):
            return queryset.none()

        latitude = float(latitude)
        longitude = float(longitude)
        distance_range = float(distance_range)

        rough_distance = (
            units.degrees(arcminutes=units.nautical(miles=distance_range)) * 2
        )

        queryset = queryset.filter(
            location__geo_lat__range=(
                latitude - rough_distance,
                latitude + rough_distance,
            ),
            location__geo_lon__range=(
                longitude - rough_distance,
                longitude + rough_distance,
            ),
        )

        cars = []
        for car in queryset:
            if car.location.geo_lat and car.location.geo_lon:
                exact_distance = distance.distance(
                    (latitude, longitude),
                    (car.location.geo_lat, car.location.geo_lon),
                ).miles

                if exact_distance <= distance_range:
                    cars.append(car)

        queryset = queryset.filter(id__in=[car.id for car in cars])
        return queryset

    # def cars_distance(self, latitude=None, longitude=None):
    #     queryset = self
    #     car_locations = []
    #     for car in queryset:
    #         if car.location.geo_lat and car.location.geo_lon:
    #             exact_distance = distance.distance(
    #                 (latitude, longitude),
    #                 (car.location.geo_lat, car.location.geo_lon),
    #             ).miles
    #             car_locations.append((car, exact_distance))

    #     return car_locations
