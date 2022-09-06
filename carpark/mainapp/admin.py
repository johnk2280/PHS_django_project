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

    def get_queryset(self, request) -> QuerySet:
        vehicles = super(VehicleAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            enterprises = Enterprise.objects.filter(
                supervisors__id=request.user.id,
            )
            vehicles = vehicles.filter(company__in=enterprises)

        return vehicles

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'company':
            kwargs['queryset'] = Enterprise.objects.filter(
                supervisors__id=request.user.id,
            )
            
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

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

    def get_queryset(self, request) -> QuerySet:
        enterprises = super(EnterpriseAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            enterprises = enterprises.filter(
                supervisors__id=request.user.id,
            )

        return enterprises


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

    def get_queryset(self, request):
        drivers = super(DriverAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            enterprises = Enterprise.objects.filter(
                supervisors__id=request.user.id,
            )
            drivers = drivers.filter(company__in=enterprises)

        return drivers

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        enterprises = Enterprise.objects.filter(
                supervisors__id=request.user.id,
            )
        if db_field.name == 'company':
            kwargs['queryset'] = enterprises
        elif db_field.name == 'vehicle':
            kwargs['queryset'] = Vehicle.objects.filter(
                company__in=enterprises,
            )

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


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
