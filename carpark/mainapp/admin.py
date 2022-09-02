from django.contrib import admin

from .models import Vehicle


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('id', 'release_date', 'mileage', 'cost')
    search_fields = ('release_date',)


