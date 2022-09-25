from django.urls import path

from authapp.views import UserLoginView
from authapp.views import EnterpriseView
from authapp.views import EnterprisesView

app_name = 'authapp'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('enterprises/', EnterprisesView.as_view(), name='enterprises'),
    path('enterprises/<int:pk>/', EnterpriseView.as_view(), name='enterprise'),
]
