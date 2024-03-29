from django.contrib import admin
from .models import Car, Location, Cargo


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("unique_number", "location", "lift_capacity")
    raw_id_fields = ("location",)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = (
        "pick_up_location",
        "delivery_location",
        "weight",
        "description",
    )
    raw_id_fields = ("pick_up_location", "delivery_location")
