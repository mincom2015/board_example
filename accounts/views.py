# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django import views
from django.contrib.auth import login as authen_login
from .forms import SignUpForm


class SignUpView(views.View):

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



