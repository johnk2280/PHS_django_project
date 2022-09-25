from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.core.paginator import EmptyPage
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
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
        vehicles = Vehicle.objects.filter(company__id=pk)
        company = Enterprise.objects.get(id=pk)
        if 'page' in request.GET:
            page = request.GET['page']
        else:
            page = 1

        paginator = Paginator(vehicles, 10)
        try:
            vehicles = paginator.page(page)
        except PageNotAnInteger:
            vehicles = paginator.page(1)
        except EmptyPage:
            vehicles = paginator.page(paginator.num_pages)

        context = {
            'vehicles': vehicles,
            'title': f'{company.name} company',
            'user': request.user,
        }
        return render(request, 'authapp/enterprise.html', context)

