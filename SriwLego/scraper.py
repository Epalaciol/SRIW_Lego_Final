import scraper_lego
import scraper_target
import django
import os
import os
import django
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from multiprocessing import Pool
from multiprocessing import cpu_count
from time import time #importamos la función time para capturar tiempos
from random import randint
import requests
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SriwLego.settings")
django.setup()

import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
from multiprocessing import cpu_count
from time import time


from recomendador.models import Producto as ProductosDjdango

if __name__ == "__main__":



##########scraper target

    tiempo_inicial = time() 

    categorias = ['architecture','city','friends','lego-batman-sets','minecraft']
    URLSResto = ['/b/lego/-/N-56h5nZ5chhkZ9imip?type=products&lnk=LEGOArchitectur','/c/lego-city/-/N-k854h?lnk=LEGOCity','/c/lego-friends/-/N-h258a?lnk=LEGOFriends','/c/lego-batman/-/N-4rt2x?lnk=LEGOBatman','/c/lego-minecraft/-/N-p2onl?lnk=LEGOminecraft']
    

    #categorias = ['architecture']
    #URLSResto = ['/b/lego/-/N-56h5nZ5chhkZ9imip?type=products&lnk=LEGOArchitectur']

    mezcla=zip(URLSResto,categorias)
    
    pool = Pool(cpu_count())

    #multiproceso para acelerar la velocidad del algoritmo (selenium es lento, sin esto tardaria unos 10 o 15 min mas)
    with pool as p:
        listas = p.map(scraper_target.legoOriginal,mezcla)
    links=[]
    lista_productos=[]
    categorias=[]
    for lista in listas:
        for element in lista:
            lista_productos.append(element)
            

    pool2 = Pool(cpu_count()*4)
    with pool2 as p:
        lista_productos=p.map(scraper_target.informacion,lista_productos)
        
    print("cantidad objetos creados")
    print(len(lista_productos))    
        
    for producto in lista_productos:
        #print(producto.to_print())

        prod= ProductosDjdango(idProducto = str(producto.codigo), nombre =producto.nombre, link1 = producto.URLBase+producto.URLResto, link2 = 'no disponible aun', categoria = producto.categoria, precio = producto.precio_venta, nPiezas = producto.piezas,observaciones = 'aun no disponible', estado =True)
        prod.save()

    tiempo_final = time() 
    tiempo_ejecucion = tiempo_final - tiempo_inicial
    
    
    print ('El tiempo de ejecucion fue:') #En segundos
    print(tiempo_ejecucion)












#scraper lego




    tiempo_inicial = time() 
    
    categoriasOficial = ['/en-us/themes/architecture','/en-us/themes/city','/en-us/themes/friends','/en-us/themes/lego-batman-sets','/en-us/themes/minecraft']

    poolLego = Pool(cpu_count()*8)

    with poolLego as p:
        listas = p.map(scraper_lego.legoOficial,categoriasOficial)
    links=[]
    lista_productos=[]
    categoriasOficial=[]
    for lista in listas:
        for element in lista:
            lista_productos.append(element)
    print("cantidad objetos creados")
    print(len(lista_productos))
    for producto in lista_productos:
        #print(producto.to_print())
       
        print(producto[1])


    tiempo_final = time() 
    tiempo_ejecucion = tiempo_final - tiempo_inicial
    
    
    print ('El tiempo de ejecucion fue:') #En segundos
    print(tiempo_ejecucion)