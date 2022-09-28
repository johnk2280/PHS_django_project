from django.contrib import messages
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Supervisor(User):
    company = models.ManyToManyField(
        'Enterprise',
        related_name='supervisors',
        verbose_name='Предприятие',
    )

    class Meta:
        verbose_name = 'Менеджер'
        verbose_name_plural = 'Менеджеры'

    def __str__(self):
        return f'{self.username}'


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

    def get_absolute_url(self) -> str:
        return reverse('authapp:vehicle_edit', kwargs={'pk': self.pk})

    # def save(self, *args, **kwargs):
    #     # TODO: переместить обработку этого случая в админку
    #
    #     if not self.drivers.filter(is_active=True):
    #         super(Vehicle, self).save(*args, **kwargs)
    #     else:
    #         messages.error(
    #             kwargs['request'],
    #             message='Невозможно переназначить предприятие, '
    #                     'т.к. за автомобилем закреплен активный водитель',
    #         )


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
        # unique=True,
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
    TZ_CHOICES = (
        ('UTC', 'UTC'),
        ('UTC+2', 'UTC+2'),
        ('UTC+3', 'UTC+3'),
        ('UTC+4', 'UTC+4'),
        ('UTC+5', 'UTC+5'),
        ('UTC+6', 'UTC+6'),
        ('UTC+7', 'UTC+7'),
        ('UTC+8', 'UTC+8'),
        ('UTC+9', 'UTC+9'),
        ('UTC+10', 'UTC+10'),
        ('UTC+11', 'UTC+11'),
        ('UTC+12', 'UTC+12'),
    )
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
    tz_info = models.CharField(
        max_length=9,
        default='UTC',
        choices=TZ_CHOICES,
        verbose_name='Часовой пояс',
    )

    class Meta:
        db_table = 'enterprises'
        verbose_name = 'Предприятие'
        verbose_name_plural = 'Предприятия'

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self) -> str:
        return reverse('authapp:enterprise', kwargs={'pk': self.pk})


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
