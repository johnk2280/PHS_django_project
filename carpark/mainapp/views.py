from django.http import HttpResponse
from django.views import View
from django.shortcuts import render


class IndexView(View):

    def get(self, request):
        context = {}
        return render(request, 'mainapp/index.html', context=context)

