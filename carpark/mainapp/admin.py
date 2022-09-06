from typing import Iterable

from django.contrib import admin
from django.db.models import QuerySet

from .models import Brand
from .models import Driver
from .models import Enterprise
from .models import Vehicle
from .models import Supervisor


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

    def get_queryset(self, request) -> Iterable:
        vehicle_qs = super(VehicleAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            vehicles = []
            enterprises = Enterprise.objects.filter(
                supervisors__id=request.user.id,
            )
            for company in enterprises:
                vehicles.extend(vehicle_qs.filter(company__id=company.id))

            return vehicles

        return vehicle_qs

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


@admin.register(Supervisor)
class ManagerAdmin(admin.ModelAdmin):
    def display_companies(self, obj: Supervisor) -> str:
        companies = map(
            lambda x: x.name,
            Enterprise.objects.filter(supervisors__id=obj.pk),
        )
        return ', '.join(companies)

    display_companies.short_description = 'Предприятия'
    list_display = ('username', 'display_companies')
