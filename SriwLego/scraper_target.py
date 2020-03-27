import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SriwLego.settings")
django.setup()

from recomendador.models import Producto as ProductosDjdango

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from multiprocessing import Pool
from multiprocessing import cpu_count
from time import time #importamos la función time para capturar tiempos
from random import randint
import requests
from time import sleep
from os import system
from selenium.webdriver.support.ui import WebDriverWait

conteo=0
URLBase = 'https://www.target.com'


##clase usada para almacenar los valores de los productos
class Producto:
    URLBase = 'https://www.target.com'

    def __init__(self, URLResto, categoria):
        self.codigo = 0
        self.categoria = categoria
        self.URLResto = URLResto
        self.nombre=""
        self.piezas=""
        self.precio_regular=""
        self.precio_venta=""
    
    def to_print(self):
    
        return "\n: codigo "+str(self.codigo)+" categoria: "+self.categoria+ "nombre: "+self.nombre+" piezas: "+str(self.piezas)+" precio regular: "+ str(self.precio_regular)+" precio venta: "+ str(self.precio_venta)
#extrae el codigo de un titulo
def extracter_codigo(titulo):
    lista_palabras = titulo.split(' ')
    for palabra in lista_palabras:
        palabra=palabra.replace(',','')
        if (palabra.isdigit() and int(palabra)>10):
            #print(titulo+"------------"+palabra)
            return palabra
    return 0

#extrae el numero de piezas quitandole el string
def extracter_piezas(titulo):
    lista_palabras = titulo.split(' ')
    for palabra in lista_palabras:
        if (palabra.isdigit()):
            return int(palabra)
    return 0

#usa bs4 para abrir la pagina del producto al que se le pasa el url
#y extrae los atributos faltantes
def informacion(producto):
    sleep(randint(0, 7))
    global conteo
    URL=producto.URLBase+producto.URLResto
    #print(URL)
    page = requests.get(URL)
    parser = BeautifulSoup(page.content, 'html.parser')


    titulo = parser.find('h1', class_='Heading__StyledHeading-sc-1m9kw5a-0').text.strip()
    #precio = parser.find('div', class_='style__PriceFontSize-gob4i1-0').text.strip()
    no_piezas  = parser.find("div", class_="Col-favj32-0 fVmltG h-padding-h-default")
    no_piezas2=no_piezas.find('div').text.strip()

    producto.nombre = titulo
    producto.codigo = extracter_codigo(titulo)
    #producto.precio  = float(precio.replace("$", ""))
    producto.piezas  = extracter_piezas(no_piezas2)

    conteo=conteo+1
    return producto




#usa selenium para renderizar las paginas que cargan mediante JS
#para conseguir algunos atributos de los productos y sus links
def legoOriginal(argumentos):

    try:
        global URLBase
        URLResto=argumentos[0]
        categoria=argumentos[1]
        listaProductos = []
        URL=URLBase+URLResto
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options)
        driver.get(URL)
        driver.find_element_by_xpath('//body').send_keys(Keys.CONTROL+Keys.END)
        sleep(15)

        page = driver.page_source

        driver.quit()
        parser = BeautifulSoup(page, 'html.parser')
        lista_productos = parser.find('ul', class_='Row-uds8za-0 bzWxaw h-padding-t-tight')
        if(lista_productos is not None):
            productos=lista_productos.find_all('div', class_='styles__StyledDetailsWrapper-e5kry1-8 dnTOUV h-display-flex h-flex-direction-col flex-grow-one full-width')
        #links_productos = lista_productos.find('a', class_='Link-sc-1khjl8b-0 styles__StyledTitleLink-e15kry1-5 cPukFm h-display-block h-text-bold h-text-bs flex-grow-one')
            if(productos is not None):
                for producto in productos:

                    link = producto.find('a')['href']
                    titulo=producto.find('a').text.strip()
                    precio_regular=producto.find('span',class_='h-text-bs').text.strip()
                    precio_promocion=producto.find('span',class_='h-text-grayDark h-text-sm h-margin-l-tiny')

                    codigo=extracter_codigo(titulo)
                    if(codigo!=0):
                        p=Producto(link,categoria)
                        if(precio_promocion is not None):
                            precio_promocion=float(precio_promocion.text.strip().replace("reg $", ""))
                            p.precio_venta=precio_promocion
                        else:
                            p.precio_venta=float(precio_regular.replace("$", ""))
                        p.precio_regular=float(precio_regular.replace("$", ""))

                        listaProductos.append(p)


        siguiente = parser.find('a', class_='Link-sc-1khjl8b-0 kTulu Button-bwu3xu-0 hHzxma ButtonWithArrow-sc-6wuvfc-0 dQFSoM')
        
        
        if(siguiente is not None):
           link_siguiente = siguiente['href']
           #print(link_siguiente)
           argumentos_nuevos=[link_siguiente,categoria]
           listaProductos.extend(legoOriginal(argumentos_nuevos))
        
            
        return listaProductos
        

    except:
        pass
        #system("taskkill /f /im  firefox.exe")
 


if __name__ == "__main__":

    tiempo_inicial = time() 

    categorias = ['architecture','city','friends','lego-batman-sets','minecraft']
    URLSResto = ['/b/lego/-/N-56h5nZ5chhkZ9imip?type=products&lnk=LEGOArchitectur','/c/lego-city/-/N-k854h?lnk=LEGOCity','/c/lego-friends/-/N-h258a?lnk=LEGOFriends','/c/lego-batman/-/N-4rt2x?lnk=LEGOBatman','/c/lego-minecraft/-/N-p2onl?lnk=LEGOminecraft']
    

    #categorias = ['architecture']
    #URLSResto = ['/b/lego/-/N-56h5nZ5chhkZ9imip?type=products&lnk=LEGOArchitectur']

    mezcla=zip(URLSResto,categorias)
    
    pool = Pool(cpu_count())

    #multiproceso para acelerar la velocidad del algoritmo (selenium es lento, sin esto tardaria unos 10 o 15 min mas)
    with pool as p:
        listas = p.map(legoOriginal,mezcla)
    links=[]
    lista_productos=[]
    categorias=[]
    for lista in listas:
        for element in lista:
            lista_productos.append(element)
            

    pool2 = Pool(cpu_count()*4)
    with pool2 as p:
        lista_productos=p.map(informacion,lista_productos)
    
    for producto in lista_productos:
        #print(producto.to_print())
        print("cantidad objetos creados")
        print(len(lista_productos))
        prod= ProductosDjdango(idProducto = str(producto.codigo), nombre =producto.nombre, link1 = producto.URLBase+producto.URLResto, link2 = 'no disponible aun', categoria = producto.categoria, precio = producto.precio_venta, nPiezas = producto.piezas,observaciones = 'aun no disponible', estado =True)
        prod.save()

    tiempo_final = time() 
    tiempo_ejecucion = tiempo_final - tiempo_inicial
    
    
    print ('El tiempo de ejecucion fue:') #En segundos
    print(tiempo_ejecucion)

