from django.urls import path
from core.views import Index


app_name = 'core'

urlpatterns = [
    path('index', Index.as_view(), name='index'),
]
