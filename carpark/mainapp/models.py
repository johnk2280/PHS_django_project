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

    class Meta:
        db_table = 'vehicles'
        verbose_name = 'Транспортное средство'
        verbose_name_plural = 'Транспортные средства'
        ordering = ('-created_at',)

    def __str__(self):
        return f'ТС {self.release_date} г.в. с пробегом {self.mileage} км' \
               f' за {self.cost} руб.'


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
        return f'{self.name} {self.car_type} ' \
               f'объем бака: {self.tank_volume}, ' \
               f'грузоподъемность: {self.load_capacity}, ' \
               f'количество мест: {self.seat_number}'

