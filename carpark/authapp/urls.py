from django.urls import path

from authapp.views import UserLoginView

app_name = 'authapp'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
]
