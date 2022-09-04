from django.contrib import admin

from .models import Vehicle
from .models import Brand


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    def display_brand(self, obj: Vehicle) -> str:
        return obj.brand

    display_brand.short_description = 'Брэнд'
    list_display = ('id', 'display_brand', 'release_date', 'mileage', 'cost')
    search_fields = ('release_date',)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'car_type',
        'tank_volume',
        'load_capacity',
        'seat_number',
    )
    search_fields = (
        'name',
        'car_type',
        'seat_number',
    )
