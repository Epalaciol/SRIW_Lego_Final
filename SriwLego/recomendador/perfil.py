import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import GridSearchCV
from recomendador.models import Producto, Calificacion, Perfil

def actualizar_perfil(usuario):
    calificaciones =  Calificacion.objects.filter(usuario_id=usuario.id)
    categorias = ['architecture','city','friends','minecraft']
    wgm = pd.DataFrame(columns=['Nombre','Precio','nPiezas','Calificacion','Categoria'])
    for cal in calificaciones:
        prod = Producto.objects.get(idProducto = cal.producto_id)
        calificacion = cal.calificacion
        wgm = wgm.append({'Nombre':prod.nombre ,'Precio': prod.precio*calificacion,'nPiezas':prod.nPiezas*calificacion ,'Calificacion': cal.calificacion,'Categoria':prod.categoria},ignore_index=True)
    for cat in categorias:
        wgm[cat] = wgm['Categoria'].apply(lambda x: 1 if x == cat else 0)
    wgm['batman'] = wgm['Categoria'].apply(lambda x: 1 if x == "lego-batman-sets" else 0)
    for cat in categorias:
        wgm[cat]= wgm[cat] * wgm.Calificacion
    wgm['batman']= wgm['batman'] * wgm.Calificacion
    #Se calculan los perfiles de las categorias

    divisor_cat = wgm.architecture.sum()+wgm.city.sum()+wgm.friends.sum()+wgm.minecraft.sum()+wgm.batman.sum()
    architecture = wgm.architecture.sum()/divisor_cat
    city = wgm.city.sum()/divisor_cat
    friends = wgm.friends.sum()/divisor_cat
    minecraft = wgm.minecraft.sum()/divisor_cat
    batman = wgm.batman.sum()/divisor_cat

    #Se calculan los perfiles para el precio y el numero de piezas
    productos = Producto.objects.all()
    
    pm = pd.DataFrame(columns=["Precio","nPiezas"])
    for pro in productos:
        pm = pm.append({"Precio":pro.precio, "nPiezas":pro.nPiezas},ignore_index=True)

    precio_aux = wgm.Precio.sum()/wgm.Calificacion.sum()
    numero_piezas_aux = wgm.nPiezas.sum()/wgm.Calificacion.sum() 
    precio = ((precio_aux-pm.Precio.min())/(pm.Precio.max()-pm.Precio.min()))
    nPiezas = ((numero_piezas_aux-pm.nPiezas.min())/(pm.nPiezas.max()-pm.nPiezas.min()))

    try:
        perfil_viejo = Perfil.objects.get(usuario_id= usuario.id)
        perfil_viejo.architecture = architecture
        perfil_viejo.city = city
        perfil_viejo.friends = friends
        perfil_viejo.minecraft = minecraft
        perfil_viejo.batman = batman
        perfil_viejo.precio = precio
        perfil_viejo.nPiezas = nPiezas
        perfil_viejo.save()
    except Perfil.DoesNotExist as e:
        Perfil.objects.create(usuario=usuario,architecture=architecture,city=city,friends=friends,minecraft=minecraft,batman=batman,precio=precio,nPiezas=nPiezas)