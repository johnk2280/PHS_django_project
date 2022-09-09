from rest_framework import status
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from mainapp.models import Enterprise
from mainapp.models import Vehicle
from mainapp.api.serializers import VehicleSerializer


class VehicleViewSet(ListModelMixin, GenericViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    # permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        vehicles = self.queryset
        if not request.user.is_superuser:
            enterprises = Enterprise.objects.filter(
                supervisors__id=request.user.id,
            )
            vehicles = vehicles.filter(company__in=enterprises)

        serializer = self.serializer_class(vehicles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

