from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import DestroyModelMixin
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from carpark.utils.data_filling import create_random_vehicles
from mainapp.models import Enterprise
from mainapp.models import Vehicle
from mainapp.api.serializers import VehicleSerializer


class VehicleViewSet(CreateModelMixin, DestroyModelMixin, ListModelMixin,
                     RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = (IsAdminUser,)

    def list(self, request, *args, **kwargs) -> Response:
        vehicles = self.queryset
        if not request.user.is_superuser:
            enterprises = Enterprise.objects.filter(
                supervisors__id=request.user.id,
            )
            vehicles = vehicles.filter(company__in=enterprises)

        serializer = self.serializer_class(vehicles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VehicleButchCreateModelViewSet(CreateModelMixin, GenericViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = (IsAdminUser,)

    def create(self, request, *args, **kwargs):
        cars = create_random_vehicles(
            enterprises=Enterprise.objects.all(),
            quantity=4,
        )
        cars = Vehicle.objects.bulk_create(cars)
        serializer = self.serializer_class(cars, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
