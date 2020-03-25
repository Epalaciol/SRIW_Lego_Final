# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date
from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth import logout

# Create your views here.

@login_required
def indexView(request):
    return render(request, "index.html")


def logoutUser(request):
   logout(request)
   return HttpResponseRedirect('/login/')   

def register(request):
    if request.method == "POST":
        try:
            user = User.objects.create_user(request.POST.get("email"), request.POST.get("email"), request.POST.get("password"),last_login= date.today())
            user.first_name = request.POST.get("name")
            user.save()
            return redirect("login")
        except IntegrityError as e: 
            if 'unique constraint' in e.message:
                return render(request, "register.html")

    return render(request, "register.html")

def recomendador(request):
    return render(request, "recomendacion.html")

def perfil(request):
    return render(request, "perfil.html")