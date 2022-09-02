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

    class Meta:
        db_table = 'vehicles'
        verbose_name = 'Транспортное средство'
        verbose_name_plural = 'Транспортные средства'
        ordering = ('-created_at',)

    def __str__(self):
        return f'ТС {self.release_date} г.в. с пробегом {self.mileage} км' \
               f' за {self.cost} руб.'



