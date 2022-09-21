from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import View

from mainapp.models import Enterprise


class UserLoginView(LoginView):
    template_name = 'authapp/login.html'

    def get_success_url(self):
        return reverse_lazy('authapp:enterprises')


class EnterpriseView(View):
    def get(self, request):
        enterprises = Enterprise.objects.filter()
        if not request.user.is_superuser:
            enterprises = Enterprise.objects.filter(
                supervisors__id=request.user.id,
            )

        context = {
            'username': request.user.username,
            'enterprises': enterprises,
        }
        return render(request, 'authapp/index.html', context)
