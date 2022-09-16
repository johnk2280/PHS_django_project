from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import DestroyModelMixin
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from carpark.utils.data_filling import create_random_drivers
from carpark.utils.data_filling import create_random_vehicles
from mainapp.models import Driver
from mainapp.models import Enterprise
from mainapp.models import Vehicle
from mainapp.api.serializers import DriverSerializer
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

        # Данное решение вопроса пагинации взял из родительского метода list()
        # класса rest_framework.mixins.ListModelMixin.
        page = self.paginate_queryset(vehicles)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(vehicles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VehicleBatchCreateModelViewSet(CreateModelMixin, GenericViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = (IsAdminUser,)

    def create(self, request, *args, **kwargs):
        quantity = int(request.data['vehicle_quantity'])
        cars = create_random_vehicles(
            enterprises=Enterprise.objects.all(),
            quantity=quantity,
        )
        cars = Vehicle.objects.bulk_create(cars)
        serializer = self.serializer_class(cars, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DriverViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = (IsAdminUser,)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        cars = Vehicle.objects.all()
        drivers = create_random_drivers(vehicles=cars)
        drivers = Driver.objects.bulk_create(drivers)
        serializer = self.serializer_class(drivers, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
