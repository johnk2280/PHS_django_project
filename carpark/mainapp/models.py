from django.contrib import messages
from django.db import models


class Vehicle(models.Model):
    cost = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name='Стоимость автомобиля, руб.',
    )
    release_date = models.DateField(
        verbose_name='Год выпуска',
        null=False,
        default='1980-10-22',
    )
    mileage = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name='Пробег, км',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    brand = models.ForeignKey(
        'Brand',
        on_delete=models.CASCADE,
        verbose_name='Название бренда',
    )
    company = models.ForeignKey(
        'Enterprise',
        on_delete=models.CASCADE,
        verbose_name='Предприятие',
        null=True,
        blank=True,
    )

    class Meta:
        db_table = 'vehicles'
        verbose_name = 'Транспортное средство'
        verbose_name_plural = 'Транспортные средства'
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.brand} {self.release_date}'

    def save(self, *args, **kwargs):
        if not self.drivers.filter(is_active=True):
            super(Vehicle, self).save(*args, **kwargs)
        else:
            messages.error(
                kwargs['request'],
                message='Невозможно переназначить предприятие, '
                'т.к. за автомобилем закреплен активный водитель',
            )


class Brand(models.Model):
    TYPE_CHOICES = (
        ('легковой', 'PASSENGER'),
        ('грузовой', 'CARGO'),
        ('тягач', 'TRUCK'),
        ('автобус', 'BUS'),
        ('спортивный', 'SPORT'),
    )
    name = models.CharField(
        max_length=50,
        unique=True,
        null=False,
        verbose_name='Название бренда',
    )
    car_type = models.CharField(
        max_length=16,
        choices=TYPE_CHOICES,
        verbose_name='Тип автомобиля',
    )
    tank_volume = models.PositiveSmallIntegerField(
        null=False,
        verbose_name='Объем бака, л',
    )
    load_capacity = models.PositiveSmallIntegerField(
        null=False,
        verbose_name='Грузоподъемность, кг',
    )
    seat_number = models.PositiveSmallIntegerField(
        null=False,
        verbose_name='Количество мест',
    )

    class Meta:
        db_table = 'brands'
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return f'{self.name} {self.car_type}'


class Enterprise(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        null=False,
        verbose_name='Название компании',
    )
    city = models.CharField(
        max_length=50,
        null=False,
        verbose_name='Город',
    )

    class Meta:
        db_table = 'enterprises'
        verbose_name = 'Предприятие'
        verbose_name_plural = 'Предприятия'

    def __str__(self):
        return f'{self.name}'


class Driver(models.Model):
    CATEGORY_CHOICES = (
        ('A', 'A'),
        ('A1', 'A1'),
        ('B', 'B'),
        ('B1', 'B1'),
        ('C', 'C'),
        ('C1', 'C1'),
        ('D', 'D'),
        ('D1', 'D1'),
        ('BE', 'BE'),
        ('CE', 'CE'),
        ('C1E', 'C1E'),
        ('DE', 'DE'),
        ('D1E', 'D1E'),
        ('M', 'M'),
        ('Tm', 'Tm'),
        ('Tb', 'Tb'),
    )
    name = models.CharField(
        max_length=50,
        unique=True,
        null=False,
        verbose_name='Имя',
    )
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        verbose_name='Автомобиль',
        null=True,
        blank=True,
        related_name='drivers',
    )
    experience = models.PositiveSmallIntegerField(
        null=False,
        verbose_name='Стаж вождения',
    )
    category = models.CharField(
        max_length=3,
        null=False,
        verbose_name='Категория прав',
        choices=CATEGORY_CHOICES,
    )
    company = models.ForeignKey(
        Enterprise,
        on_delete=models.CASCADE,
        verbose_name='Предприятие',
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name='Активен',
    )

    class Meta:
        db_table = 'drivers'
        verbose_name = 'Водитель'
        verbose_name_plural = 'Водители'

    def __str__(self):
        return f'{self.name}'
