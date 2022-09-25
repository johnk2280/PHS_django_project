from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import View

from mainapp.models import Vehicle
from mainapp.models import Enterprise


class UserLoginView(LoginView):
    template_name = 'authapp/login.html'

    def get_success_url(self):
        return reverse_lazy('authapp:enterprises')


class EnterprisesView(View):
    def get(self, request) -> render:
        enterprises = Enterprise.objects.filter()
        if not request.user.is_superuser:
            enterprises = Enterprise.objects.filter(
                supervisors__id=request.user.id,
            )

        context = {
            'username': request.user.username,
            'enterprises': enterprises,
        }
        return render(request, 'authapp/enterprises.html', context)


class EnterpriseView(View):
    def get(self, request, pk) -> render:
        vehicles = Vehicle.objects.filter(company__id=pk)[:10]
        company = Enterprise.objects.get(id=pk)
        context = {
            'vehicles': vehicles,
            'title': f'{company.name} company',
            'user': request.user,
        }
        # TODO: пагинация
        return render(request, 'authapp/enterprise.html', context)

