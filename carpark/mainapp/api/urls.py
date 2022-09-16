from django.urls import include
from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import DriverViewSet
from .views import VehicleViewSet
from .views import VehicleBatchCreateModelViewSet

app_name = 'mainapp'

router = DefaultRouter()
router.register('vehicles', VehicleViewSet, basename='vehicles')
router.register('drivers', DriverViewSet, basename='drivers')
router.register(
    'create_vehicles',
    VehicleBatchCreateModelViewSet,
    basename='create_vehicles',
)

urlpatterns = [
    path('', include(router.urls)),
]

