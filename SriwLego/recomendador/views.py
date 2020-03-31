# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date
from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth import logout
from recomendador.models import Producto, Calificacion, Perfil
from recomendador.rate import recomendacion
from recomendador.perfil import actualizar_perfil

# Create your views here.

@login_required
def indexView(request):
    usuario_actual = User.objects.get(username = request.user)
    if request.method == "POST":
        if(request.POST.get("architecture") is None):
            producto_obj = Producto.objects.get(idProducto=request.POST.get("idProducto"))
            calificacion_usuario = request.POST.get("calificacion")
            try:
                calificacion_vieja = Calificacion.objects.get(usuario_id= usuario_actual.id, producto_id = request.POST.get("idProducto"))
                calificacion_vieja.calificacion = calificacion_usuario
                calificacion_vieja.save()
            except Calificacion.DoesNotExist as e:
                Calificacion.objects.create(producto = producto_obj, calificacion= calificacion_usuario, usuario = usuario_actual)
        else:
            try:
                perfil = Perfil.objects.get(usuario_id= usuario_actual.id)
            except Perfil.DoesNotExist as e:
                Perfil.objects.create(usuario = usuario_actual,
                architecture = request.POST.get("architecture"),
                city = request.POST.get("city"),
                friends = request.POST.get("friends"),
                batman = request.POST.get("batman"),
                minecraft = request.POST.get("minecraft"),
                precio = request.POST.get("precio"),
                nPiezas = request.POST.get("piezas"))
            
    prod = Producto.objects.all().filter(estado=True)

    for producto in prod:
        try:
            calificacion_vieja = Calificacion.objects.get(usuario_id= usuario_actual.id, producto_id = producto.idProducto)
            producto.calificacion_vieja = calificacion_vieja.calificacion
        except Calificacion.DoesNotExist as e:
            producto.calificacion_vieja = '-'
    try:
        perfil = Perfil.objects.get(usuario_id= usuario_actual.id)
        return render(request, "index.html", {'productos' : prod})
    except Perfil.DoesNotExist as e:
        return render(request, "perfilNuevo.html")
    


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
    usuario_actual = User.objects.get(username = request.user)
    productos = recomendacion(usuario_actual)
    return render(request, "recomendacion.html", {'productos' : productos[0][0:5]})

def perfil(request):
    usuario_actual = User.objects.get(username = request.user)
    perfil = Perfil.objects.get(usuario_id = usuario_actual.id)
    return render(request, "perfil.html",{'perfil':perfil})