from django.urls import path
from authentication.views import Login, Logout


app_name = 'authentication'

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
]
