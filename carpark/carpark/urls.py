from django.contrib import admin
from django.urls import include
from django.urls import path

from rest_framework.authtoken import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', views.obtain_auth_token),
    path('api/v1/', include('mainapp.api.urls')),
    path('auth/', include('authapp.urls')),
]
