from faker import Faker
import random
from django.db.models import Max
from apps.service_delivery.models import Location


def get_random_location(number: int = 20) -> list[Location]:
    locations = []
    max_id = Location.objects.all().aggregate(max_id=Max("id"))["max_id"]
    for _ in range(number):
        while True:
            pk = random.randint(1, max_id)
            location = Location.objects.filter(pk=pk).first()
            if location:
                locations.append(location)
                break
    return locations


def get_fake_number(number: int):
    fake = Faker()
    numbers = [
        str(fake.random.randint(1000, 9999)) + fake.random_uppercase_letter()
        for _ in range(number)
    ]
    return numbers


def get_fake_lift_capacity(number: int):
    fake = Faker()
    numbers = [fake.random.randint(1, 999) for _ in range(number)]
    return numbers
