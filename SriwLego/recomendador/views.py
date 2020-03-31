# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date
from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth import logout
from recomendador.models import Producto, Calificacion, Perfil, Acertado
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
    if request.method == "POST":
        valor1 = request.POST.get("gusto1")
        if(valor1 is not None):
            if(valor1 == 'si'):
                Acertado.objects.create(acertado = True, usuario = usuario_actual)
            else:
                Acertado.objects.create(acertado = False, usuario = usuario_actual)
        valor2 = request.POST.get("gusto2")
        if(valor2 is not None):
            if(valor2 == 'si'):
                Acertado.objects.create(acertado = True, usuario = usuario_actual)
            else:
                Acertado.objects.create(acertado = False, usuario = usuario_actual)
        valor3 = request.POST.get("gusto3")
        if(valor3 is not None):
            if(valor3 == 'si'):
                Acertado.objects.create(acertado = True, usuario = usuario_actual)
            else:
                Acertado.objects.create(acertado = False, usuario = usuario_actual)
        valor4 = request.POST.get("gusto4")
        if(valor4 is not None):
            if(valor4 == 'si'):
                Acertado.objects.create(acertado = True, usuario = usuario_actual)
            else:
                Acertado.objects.create(acertado = False, usuario = usuario_actual)
        valor5 = request.POST.get("gusto5")
        if(valor5 is not None):
            if(valor5 == 'si'):
                Acertado.objects.create(acertado = True, usuario = usuario_actual)
            else:
                Acertado.objects.create(acertado = False, usuario = usuario_actual)
        valor6 = request.POST.get("gusto6")
        if(valor6 is not None):
            if(valor6 == 'si'):
                Acertado.objects.create(acertado = True, usuario = usuario_actual)
            else:
                Acertado.objects.create(acertado = False, usuario = usuario_actual)
        valor7 = request.POST.get("gusto7")
        if(valor7 is not None):
            if(valor7 == 'si'):
                Acertado.objects.create(acertado = True, usuario = usuario_actual)
            else:
                Acertado.objects.create(acertado = False, usuario = usuario_actual)
        valor8 = request.POST.get("gusto8")
        if(valor8 is not None):
            if(valor8 == 'si'):
                Acertado.objects.create(acertado = True, usuario = usuario_actual)
            else:
                Acertado.objects.create(acertado = False, usuario = usuario_actual)
        valor9 = request.POST.get("gusto9")
        if(valor9 is not None):
            if(valor9 == 'si'):
                Acertado.objects.create(acertado = True, usuario = usuario_actual)
            else:
                Acertado.objects.create(acertado = False, usuario = usuario_actual)
        valor10 = request.POST.get("gusto10")
        if(valor10 is not None):
            if(valor10 == 'si'):
                Acertado.objects.create(acertado = True, usuario = usuario_actual)
            else:
                Acertado.objects.create(acertado = False, usuario = usuario_actual)
        if(request.POST.get("idProducto") is not None):
            producto_obj = Producto.objects.get(idProducto=request.POST.get("idProducto"))
            calificacion_usuario = request.POST.get("calificacion")
            try:
                calificacion_vieja = Calificacion.objects.get(usuario_id= usuario_actual.id, producto_id = request.POST.get("idProducto"))
                calificacion_vieja.calificacion = calificacion_usuario
                calificacion_vieja.save()
            except Calificacion.DoesNotExist as e:
                Calificacion.objects.create(producto = producto_obj, calificacion= calificacion_usuario, usuario = usuario_actual)

    usuario_actual = User.objects.get(username = request.user)
    productos = recomendacion(usuario_actual)
    lista = productos[0][0:10]
    n = 1
    for prod in lista:
        prod["producto"].n = n
        n += 1
    return render(request, "recomendacion.html", {'productos' : lista})

def perfil(request):
    usuario_actual = User.objects.get(username = request.user)
    perfil = Perfil.objects.get(usuario_id = usuario_actual.id)
    return render(request, "perfil.html",{'perfil':perfil})