from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelform_factory
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.core.paginator import EmptyPage
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView

from .forms import VehicleForm

from mainapp.models import Vehicle
from mainapp.models import Enterprise


class UserLoginView(LoginView):
    template_name = 'authapp/login.html'

    def get_success_url(self):
        return reverse_lazy('authapp:enterprises')


class EnterprisesView(LoginRequiredMixin, View):
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


class EnterpriseView(LoginRequiredMixin, View):
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


class VehicleEditView(LoginRequiredMixin, UpdateView):
    model = Vehicle
    fields = '__all__'
    template_name = 'authapp/vehicle_form.html'
    success_url = reverse_lazy('authapp:enterprises')

    # def get_context_data(self, **kwargs):
    #     data = super(VehicleEditView, self).get_context_data(**kwargs)
    #     VehicleModelForm = modelform_factory(
    #         Vehicle,
    #         form=VehicleForm,
    #     )
    #
    #     model_form = VehicleModelForm(self.request.POST)
    #
    #     data['vehicle'] = model_form
    #     return data
