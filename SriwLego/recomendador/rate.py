import pandas as pd
import math 
import numpy as np
from surprise import Dataset, Reader, SVD
from surprise.model_selection import GridSearchCV
from recomendador.models import Producto, Calificacion, Perfil

def recomendacion(usuario):
    recomendaciones_colaborativo = recomendar_colaborativo(usuario)
    recomendaciones_contenido = recomendar_contenido(usuario)
    return [recomendaciones_colaborativo,recomendaciones_contenido]

def recomendar_contenido (usuario):
    perfil = Perfil.objects.get(usuario_id=usuario.id)
    productos = Producto.objects.all()
    calificaciones =  Calificacion.objects.filter(usuario_id=usuario.id)
        
    pm = pd.DataFrame(columns=["Precio","nPiezas"])
    for pro in productos:
        pm = pm.append({"Precio":pro.precio, "nPiezas":pro.nPiezas},ignore_index=True)

    calificados = []
    for cal in calificaciones:
        calificados.append(cal.producto_id)
    
    wgm = pd.DataFrame(columns=['id','Nombre','Precio','nPiezas','Categoria'])
    
    #Se escogen los productos no calificados
    for pro in productos:
        if(not(pro.idProducto in calificados)):
            wgm = wgm.append({'id':pro.idProducto,
                            'Nombre':pro.nombre ,
                            'Precio': ((pro.precio-pm.Precio.min())/(pm.Precio.max()-pm.Precio.min())),
                            'nPiezas':((pro.nPiezas-pm.nPiezas.min())/(pm.nPiezas.max()-pm.nPiezas.min())),
                            'Categoria':pro.categoria},ignore_index=True)
    
    categorias = ['architecture','city','friends','minecraft']
    for cat in categorias:
        wgm[cat] = wgm['Categoria'].apply(lambda x: 1 if x == cat else 0)
    wgm['batman'] = wgm['Categoria'].apply(lambda x: 1 if x == "lego-batman-sets" else 0)

    wgm['distancia_euclidiana'] = (((perfil.architecture-wgm.architecture)**2)+
                                    ((perfil.city-wgm.city)**2)+
                                    ((perfil.friends-wgm.friends)**2)+
                                    ((perfil.batman-wgm.batman)**2)+
                                    ((perfil.minecraft-wgm.minecraft)**2)+
                                    ((perfil.precio-wgm.Precio)**2)+
                                    ((perfil.nPiezas-wgm.nPiezas)**2))**0.5
    
    wgm = wgm.sort_values('distancia_euclidiana', ascending=True)
    productos_rec = []
    for elemento in wgm.id:
        productos_rec.append({'producto':productos.get(idProducto=int(elemento))})
    productos_rec
    return productos_rec

def recomendar_colaborativo (usuario):
    array = []
    for rate in Calificacion.objects.all():
        array.append([rate.usuario_id, rate.producto_id, rate.calificacion])
    
    df = pd.DataFrame(data=array)
    reader = Reader(rating_scale=(0, 10))
    data = Dataset.load_from_df(df, reader)
    trainingSet = data.build_full_trainset()
    param_grid = {
        'n_factors':[50,100,150],
        "n_epochs": [40,50,60],
        "lr_all": [0.002, 0.005],
        "reg_all": [0.4, 0.6]
    }

    gs = GridSearchCV(SVD, param_grid, measures=["rmse", "mae"], cv=3)
    gs.fit(data)
    #Parametros optimos
    params = gs.best_params["rmse"]
    SVDoptimized = SVD(n_factors=params['n_factors'], n_epochs=params['n_epochs'],lr_all=params['lr_all'], reg_all=params['reg_all'])
    SVDoptimized.fit(trainingSet)

    prod = Producto.objects.all()

    prod_user = Calificacion.objects.all().filter(usuario_id = usuario.id)

    #Productos sin calificar
    productos_SinC = []
    for producto in prod:
        encontrado = False
        for producto_usuario in prod_user:
            if (producto_usuario.producto_id == producto.idProducto):
                encontrado = True
        if (not encontrado):
            productos_SinC.append(producto)

    #productos_recomendados
    productos_rec = []

    for producto in productos_SinC:
        productos_rec.append({'producto': producto, 'svd': SVDoptimized.predict(usuario.id, producto.idProducto).est})

    def ordenador(e):
        return e['svd']
    
    productos_rec.sort(reverse=True, key=ordenador)

    return productos_rec