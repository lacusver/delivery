from django.db import models
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator,
)
from .service.geopy_manager import GeoQuerySet


class Location(models.Model):
    city = models.CharField(verbose_name="Город", max_length=255)
    state = models.CharField(verbose_name="Штат", max_length=255)
    zip_code = models.CharField(
        verbose_name="Почтовый индекс", max_length=255, unique=True
    )
    geo_lat = models.DecimalField(
        max_digits=19, decimal_places=16, verbose_name="Широта", db_index=True
    )
    geo_lon = models.DecimalField(
        max_digits=19, decimal_places=16, verbose_name="Долгота", db_index=True
    )

    def __str__(self) -> str:
        return f"{self.zip_code}"

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"


class Car(models.Model):
    unique_number = models.CharField(
        verbose_name="Уникальный номер",
        unique=True,
        max_length=5,
        validators=[
            RegexValidator(
                regex="^\\d{4}[A-Z]$",
                message="цифра 1000-9999+заглавная буква английского алфавита",
                code="nomatch",
            )
        ],
    )
    location = models.ForeignKey(
        Location,
        to_field="zip_code",
        on_delete=models.SET_NULL,
        related_name="cars",
        blank=False,
        null=True,
        verbose_name="Текущая локация",
    )
    lift_capacity = models.FloatField(
        verbose_name="Грузоподъемность",
        validators=[MinValueValidator(1), MaxValueValidator(1000)],
    )
    objects = models.Manager()
    geo_objects = GeoQuerySet.as_manager()

    def __str__(self) -> str:
        return f"{self.unique_number}"

    class Meta:
        verbose_name = "Машина"
        verbose_name_plural = "Машины"


class Cargo(models.Model):
    pick_up_location = models.ForeignKey(
        Location,
        to_field="zip_code",
        on_delete=models.SET_NULL,
        related_name="cargo_pick_up",
        blank=False,
        null=True,
        verbose_name="Локация pick-up",
    )
    delivery_location = models.ForeignKey(
        Location,
        to_field="zip_code",
        on_delete=models.SET_NULL,
        related_name="cargo_delivery",
        blank=False,
        null=True,
        verbose_name="Локация доставки",
    )
    weight = models.FloatField(
        verbose_name="Вес",
        validators=[MinValueValidator(1), MaxValueValidator(1000)],
    )
    description = models.CharField(verbose_name="Описание", max_length=255)

    def __str__(self) -> str:
        return f"{self.description}"

    class Meta:
        verbose_name = "Груз"
        verbose_name_plural = "Грузы"
