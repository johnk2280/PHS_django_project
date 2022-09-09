from django.urls import include
from django.urls import path

from rest_framework.routers import DefaultRouter

from mainapp.api.views import VehicleViewSet

app_name = 'mainapp'

router = DefaultRouter()
router.register('vehicles', VehicleViewSet, basename='vehicles')

urlpatterns = [
    path('', include(router.urls)),
]

