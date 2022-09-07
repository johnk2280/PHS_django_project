from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet


from .models import Vehicle
from .serializers import VehicleSerializer


class VehicleViewSet(ListModelMixin, GenericViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

