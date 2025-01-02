from django.shortcuts import HttpResponse
from django.views import View


class Index(View):
    def get(self, request):
        return HttpResponse('Core')
