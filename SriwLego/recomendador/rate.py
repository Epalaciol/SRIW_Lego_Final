import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import GridSearchCV
from recomendador.models import Producto, Calificacion, Perfil

def recomendacion(usuario):
    recomendaciones_colaborativo = recomendar_colaborativo(usuario)
    recomendaciones_contenido = recomendar_contenido(usuario)
    return [recomendaciones_colaborativo,recomendaciones_contenido]

def recomendar_contenido (usuario):

    productos_rec = []
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