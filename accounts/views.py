# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.views.generic import View, UpdateView
from django.contrib.auth import login as authen_login
from .forms import SignUpForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy


class SignUpView(View):

    def get(self, request):
        form = SignUpForm()
        return render(request, 'accounts/signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            authen_login(request, user)
            return redirect('board')
        return render(request, 'accounts/signup.html', {'form': form})


class UpdateAccountView(UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email', ]
    template_name = 'accounts/my_account.html'
    success_url = reverse_lazy('my_account')

    def get_object(self, queryset=None):
        return self.request.user
