from dataclasses import dataclass
from apps.service_delivery.models import Cargo, Car
from typing import List


@dataclass
class CargoListDTO:
    cargo: Cargo
    car_amount: int


@dataclass
class CarListDTO:
    car: Car
    car_distance: float


@dataclass
class CargoDistancesDTO:
    cargo: Cargo
    cars: List[CarListDTO]
