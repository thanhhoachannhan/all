import os, sys, time, signal, shutil
from django.urls import path, include, reverse
from django.conf import settings
from django.shortcuts import HttpResponse, render
from django.contrib import admin
from django.template import Context, Template


settings.SILENCED_SYSTEM_CHECKS=['admin.W411']
signal.signal(signal.SIGINT, lambda sig, frame: (shutil.rmtree('__pycache__', ignore_errors=True), sys.exit(0)))

def htmx_render(request, template, base_template=None, context={}):
    if request.htmx or not base_template: return render(request, template, context)
    template = Template(f"""{{% extends "{base_template}" %}}\n{{% block content %}}\n\t{{% include "{template}" %}}\n{{% endblock content %}}""")
    return HttpResponse(template.render(Context(context)))

def index(request): return render(request, 'index.html')
def home(request): return htmx_render(request, 'home.html', 'index.html')
def about(request): return htmx_render(request, 'about.html', 'index.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('home/', home, name='home'),
    path('about/', about, name='about'),
]