import random
from datetime import datetime
from datetime import timedelta
from typing import Iterable
from typing import Union
from typing import List

from django.db.models import Model
from django.db.models import QuerySet

from mainapp.models import Driver
from mainapp.models import Brand
from mainapp.models import Vehicle

BRANDS = (
    'KIA', 'HYUNDAI', 'SCANIA', 'VOLVO', 'MERCEDES-BENZ', 'LADA', 'TIGER',
    'TOYOTA', 'MAZDA', 'VW', 'SCODA', 'GAZELLE', 'FORD', 'PEUGEOT', 'MAZDA',
    'NISSAN', 'RENAULT', 'ECOPLAN',
)
CAR_TYPES = ('легковой', 'грузовой', 'тягач', 'автобус', 'спортивный')
CATEGORIES = (
    'A', 'A1', 'B', 'B1', 'C', 'C1', 'D', 'D1', 'BE', 'CE', 'C1E', 'DE', 'D1E',
    'M', 'Tm', 'Tb',
)
NAMES = (
    'Василий', 'Андрей', 'Михаил', 'Петр', 'Сергей', 'Евгений', 'Александр',
    'Кирилл', 'Макс', 'Авитис', 'Карен', 'Артем',
)
SURNAMES = (
    'Сильный', 'Умный', 'Шустрый', 'Проворный', 'Сообразительный',
    'Находчивый', 'Стойкий',
)


def get_random_date() -> datetime.date:
    start = datetime.strptime('2000-01-01', '%Y-%m-%d').date()
    return start + timedelta(days=random.randint(1, 8000))


def create_random_brand() -> Model:
    car_type = random.choice(CAR_TYPES)
    tank_volume = random.randint(
        50,
        70 if car_type in ('легковой', 'спортивный') else 500,
    )
    load_capacity = random.randint(
        1200 if car_type in ('легковой', 'спортивный') else 5000,
        2000 if car_type in ('легковой', 'спортивный') else 30000,
    )
    seat_number = random.randint(
        2 if car_type not in ('автобус',) else 12,
        4 if car_type not in ('автобус',) else 36,
    )
    brand = Brand(
        name=random.choice(BRANDS),
        car_type=car_type,
        tank_volume=tank_volume,
        load_capacity=load_capacity,
        seat_number=seat_number,
    )
    brand.save()
    return brand


def create_random_vehicles(
        enterprises: Union[List, QuerySet],
        quantity: int,
) -> Iterable[Model]:
    vehicles = []
    for company in enterprises:
        vehicles.extend(
            map(
                lambda x: Vehicle(
                    cost=random.randint(100_000, 10_000_000),
                    release_date=get_random_date(),
                    mileage=random.randint(1_000, 1_000_000),
                    brand=create_random_brand(),
                    company=company,
                ),
                range(quantity)
            )
        )

    return vehicles


def create_random_drivers(vehicles: Union[List, QuerySet]) -> Iterable[Model]:
    drivers = map(
        lambda car: Driver(
            name=f'{random.choice(NAMES)} {random.choice(SURNAMES)}',
            vehicle=car,
            experience=random.randint(1, 40),
            category=random.choice(CATEGORIES),
            company=car.company,
            is_active=True if random.randint(0, 10) % 10 == 0 else False,
        ),
        vehicles
    )
    return drivers
