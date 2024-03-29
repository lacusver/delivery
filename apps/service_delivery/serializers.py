from rest_framework import serializers
from .models import Cargo, Car, Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class CargoSerializer(serializers.ModelSerializer):
    pick_up_location = LocationSerializer(read_only=True)
    delivery_location = LocationSerializer(read_only=True)

    class Meta:
        model = Cargo
        fields = "__all__"
        read_only_fields = ("pick_up_location", "delivery_location")


class CargoListSerializer(serializers.Serializer):
    cargo = CargoSerializer()
    car_amount = serializers.IntegerField()


class CargoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = "__all__"
        extra_kwargs = {
            "pick_up_location": {"required": True},
            "delivery_location": {"required": True},
        }


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = "__all__"
        extra_kwargs = {"location": {"required": True, "allow_null": False}}


class CarDistanceListSerializer(serializers.Serializer):
    car = CarSerializer()
    car_distance = serializers.FloatField()


class CargoDetailSerializer(serializers.Serializer):
    cargo = CargoSerializer()
    cars = CarDistanceListSerializer(many=True)
