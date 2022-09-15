from django.urls import include
from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import VehicleViewSet
from .views import VehicleButchCreateModelViewSet

app_name = 'mainapp'

router = DefaultRouter()
router.register('vehicles', VehicleViewSet, basename='vehicles')
router.register(
    'create_vehicles',
    VehicleButchCreateModelViewSet,
    basename='create_vehicles',
)

urlpatterns = [
    path('', include(router.urls)),
]
