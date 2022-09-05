from django.contrib import admin

from .models import Brand
from .models import Driver
from .models import Enterprise
from .models import Vehicle


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    def display_brand(self, obj: Vehicle) -> str:
        return obj.brand

    def display_company(self, obj: Vehicle) -> str:
        return obj.company

    display_brand.short_description = 'Брэнд'
    display_company.short_description = 'Предприятие'
    list_display = (
        'id',
        'display_brand',
        'release_date',
        'mileage',
        'cost',
        'display_company',
    )
    search_fields = ('release_date', 'company__name')

    def save_model(self, request, obj, form, change):
        # TODO: при сохранении в модели должна проходить проверка на то,
        #  назначен ли активный водитель на автомобиль. Если назначен,
        #  то должно вызываться исключение, которое будет обрабатываться здесь.
        #  С выводом необходимого сообщения.
        obj.save(request=request)


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


@admin.register(Enterprise)
class EnterpriseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city')
    search_fields = ('name', 'city')


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    def display_company(self, obj: Driver) -> str:
        return obj.company.name

    def display_vehicle(self, obj: Driver) -> str:
        return obj.vehicle

    display_company.short_description = 'Предприятие'
    display_vehicle.short_description = 'Автомобиль'

    list_display = (
        'id',
        'name',
        'category',
        'experience',
        'company',
        'vehicle',
        'is_active',
    )
    search_fields = ('id', 'name', 'company', 'vehicle', 'category')
