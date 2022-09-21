from django.urls import path

from authapp.views import UserLoginView
from authapp.views import EnterpriseView

app_name = 'authapp'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('enterprises/', EnterpriseView.as_view(), name='enterprises'),
]
