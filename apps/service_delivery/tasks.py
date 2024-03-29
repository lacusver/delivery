from django.db import transaction
from apps.service_delivery.models import Car
from utils.repository_fake.repository import get_random_location
from delivery.celery import app


@app.task()
def update_car_location():
    cars = Car.objects.select_for_update()
    locations = get_random_location(cars.count())
    with transaction.atomic():
        for i, car in enumerate(cars):
            car.location = locations[i]
            car.save()
    return True
