# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from datetime import date
# Create your views here.

def indexView(request):
    return render(request, "index.html")

def login(request):
    return render(request, "login.html")

def register(request):
    if request.method == "POST":
        user = User.objects.create_user(request.POST.get("email"), request.POST.get("email"), request.POST.get("password"),last_login= date.today())
        user.first_name = request.POST.get("name")
        user.save()
        return redirect("login")
    return render(request, "register.html")