from django.urls import path

from authapp.views import UserLoginView
from authapp.views import EnterpriseView
from authapp.views import EnterprisesView
from authapp.views import VehicleEditView

app_name = 'authapp'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('enterprises/', EnterprisesView.as_view(), name='enterprises'),
    path('enterprises/<int:pk>/', EnterpriseView.as_view(), name='enterprise'),
    path('vehicles/<int:pk>/', VehicleEditView.as_view(), name='vehicle_edit'),
]
