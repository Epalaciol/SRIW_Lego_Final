# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.

#Lego
class Producto(models.Model):
    idProducto = models.CharField(max_length=50, primary_key=True)
    nombre = models.CharField(max_length=60)
    link1 = models.URLField()
    link2 = models.URLField(null = True)
    categoria =  models.CharField(max_length=50)
    precio = models.FloatField()
    nPiezas = models.IntegerField()
    observaciones = models.TextField(null = True)
    estado = models.BooleanField()


#Clase que almacena los productos acertados del sistema
class Acertado(models.Model):
    acertado = models.BooleanField()
    usuario =  models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

#Perfil generado de recomendacion del usuario
class Perfil(models.Model):
    usuario =  models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    architecture = models.FloatField()
    city = models.FloatField()
    friends = models.FloatField()
    batman = models.FloatField()
    minecraft = models.FloatField()
    precio = models.FloatField()
    nPiezas = models.FloatField()


#Clase que asocia el producto el usuario y la calificacion otorgada
class Calificacion(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE,)
    calificacion = models.IntegerField()
    usuario =  models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

