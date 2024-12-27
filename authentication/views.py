from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from authentication.forms import LoginForm


class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('core:index'))
        return render(request, 'login.html', {
            'form': LoginForm()
        })
    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(username)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'core:index')
                return redirect(next_url)
        else:
            print('form is not valid')
            print(form.error_messages)
        return redirect(reverse('authentication:login'))

class Logout(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        next_url = request.GET.get('next', '/')
        return redirect(next_url)
