import os
import django
import requests
from bs4 import BeautifulSoup

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SriwLego.settings")
django.setup()

from recomendador.models import Producto as ProductosDjdango
import scraper_target
from multiprocessing import Pool
from multiprocessing import cpu_count
from time import time #importamos la función time para capturar tiempos
<<<<<<< HEAD

from recomendador.models import Producto as ProductosDjdango

URLBaseLego =  'https://www.lego.com'

def informacionOficial(URLP):
    global URLBaseLego
    URLProducto = URLBaseLego 
    URLProducto += URLP
    pagina = requests.get(URLProducto)
    parser = BeautifulSoup(pagina.content, 'html.parser')
    listarPiezas = parser.find_all('div', class_='ProductDetailsstyles__ProductAttribute-sc-16lgx7x-2 vcPOs')
    try:
        piezas  = listarPiezas[1].find_all('span')
        piezas = piezas[1]
        piezas = piezas.text.strip()
    except IndexError:
        piezas = 0
    return piezas, URLProducto

def legoOficial(listaLego):
    global URLBaseLego

    URL = URLBaseLego
    URL += listaLego
    categoria = listaLego[14:]
    try:
        categoria = categoria.split('?')
        categoria = categoria[0]
    except:
        pass
=======
from random import randint
import requests
from time import sleep
from os import system
from selenium.webdriver.support.ui import WebDriverWait

conteo=0
URLBase = 'https://www.target.com'
URLBaseLego =  'https://www.lego.com'


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
>>>>>>> 7c37c163dfb537f43f55c219269573aee641bf73
    page = requests.get(URL)
    parser = BeautifulSoup(page.content, 'html.parser')
    lista_productos = parser.find('div', class_='ProductListingsstyles__Content-sc-1taio5c-2 iHRYuT')
    productos = lista_productos.find_all('div', class_='ProductLeafSharedstyles__Wrapper-sc-1epu2xb-0 hIVRQm')
    listaGeneral =[]

    for producto in   productos:
        URL = producto.find('a', class_= 'ProductImagestyles__ProductImageLink-sc-1sgp7uc-0 hoRfhG')['href']
        nombre = producto.find('h2', class_='ProductLeafSharedstyles__Title-sc-1epu2xb-9 eNbUrI Text__BaseText-aa2o0i-0 zdErV')
        nombre = nombre.find('span', class_='Markup__StyledMarkup-ar1l9g-0 bTYWAd')
        identificador = producto.find('span', class_= 'ProductLeafSharedstyles__Code-sc-1epu2xb-8 fqevBI Text__BaseText-aa2o0i-0 fZPGmf')
        precio = producto.find('span', class_= "ProductPricestyles__StyledText-vmt0i4-0 ipNtqe Text__BaseText-aa2o0i-0 kCXVdj")
        try:
            precio = precio.text.strip()
            indice = precio.find('Price')
            precioFinal= precio[indice:]
            precioFinal = precioFinal[6:]
        except  AttributeError:
            precio = producto.find('div', class_= "ProductPricestyles__Wrapper-vmt0i4-1 kDSLfg")
            precio = precio.find_all('span')
            precio = precio[2].text.strip()
            indice = precio.find('Price')
            precioFinal= precio[indice:]
            precioFinal = precioFinal[6:]
        except:
            pass      
        

        listaInformacion = informacionOficial(URL)
        piezas = listaInformacion[0]
        enlaceProducto =listaInformacion[1]

        identificador = identificador.text.strip()
        nombre = nombre.text.strip()
        if (len(identificador)>=10):            
            identificador = identificador.split('.')
            identificador = identificador[0]

        #print(identificador, nombre, enlaceProducto,categoria,precioFinal,piezas)
        listaGeneral.append((identificador, nombre, enlaceProducto,categoria,precioFinal,piezas ))
    
    
    lista_paginas = parser.find('nav', class_='Paginationstyles__PagesNav-npbsev-2 hYNPJr')
    if str(type(lista_paginas)) == "<class 'bs4.element.Tag'>":
        paginas = lista_paginas.find_all('a', class_ ='Paginationstyles__NextLink-npbsev-10 ewFiGQ')
        for pagina in paginas:
            listaGeneral.extend(legoOficial(pagina['href']))

    return listaGeneral      
    

if __name__ == "__main__":
    tiempo_inicial = time() 



    
    categoriasOficial = ['/en-us/themes/architecture','/en-us/themes/city','/en-us/themes/friends','/en-us/themes/lego-batman-sets','/en-us/themes/minecraft']

<<<<<<< HEAD
    poolLego = Pool(cpu_count()*8)
=======
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
>>>>>>> 7c37c163dfb537f43f55c219269573aee641bf73

    with poolLego as p:
        listas = p.map(legoOficial,categoriasOficial)
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

<<<<<<< HEAD

 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
=======
def informacionOficial(URLP):
    global URLBaseLego
    URLProducto = URLBaseLego 
    URLProducto += URLP
    pagina = requests.get(URLProducto)
    parser = BeautifulSoup(pagina.content, 'html.parser')
    listarPiezas = parser.find_all('div', class_='ProductDetailsstyles__ProductAttribute-sc-16lgx7x-2 vcPOs')
    try:
        piezas  = listarPiezas[1].find_all('span')
        piezas = piezas[1]
        piezas = piezas.text.strip()
    except IndexError:
        piezas = 0
    return piezas, URLProducto


def legoOficial(listaLego):
    global URLBaseLego

    URL = URLBaseLego
    URL += listaLego
    categoria = listaLego[14:]
    try:
        categoria = categoria.split('?')
        categoria = categoria[0]
    except:
        pass
    page = requests.get(URL)
    parser = BeautifulSoup(page.content, 'html.parser')
    lista_productos = parser.find('div', class_='ProductListingsstyles__Content-sc-1taio5c-2 iHRYuT')
    productos = lista_productos.find_all('div', class_='ProductLeafSharedstyles__Wrapper-sc-1epu2xb-0 hIVRQm')
    listaGeneral =[]

    for producto in   productos:
        URL = producto.find('a', class_= 'ProductImagestyles__ProductImageLink-sc-1sgp7uc-0 hoRfhG')['href']
        nombre = producto.find('h2', class_='ProductLeafSharedstyles__Title-sc-1epu2xb-9 eNbUrI Text__BaseText-aa2o0i-0 zdErV')
        nombre = nombre.find('span', class_='Markup__StyledMarkup-ar1l9g-0 bTYWAd')
        identificador = producto.find('span', class_= 'ProductLeafSharedstyles__Code-sc-1epu2xb-8 fqevBI Text__BaseText-aa2o0i-0 fZPGmf')
        precio = producto.find('span', class_= "ProductPricestyles__StyledText-vmt0i4-0 ipNtqe Text__BaseText-aa2o0i-0 kCXVdj")
        try:
            precio = precio.text.strip()
            indice = precio.find('Price')
            precioFinal= precio[indice:]
            precioFinal = precioFinal[6:]
        except  AttributeError:
            precio = producto.find('div', class_= "ProductPricestyles__Wrapper-vmt0i4-1 kDSLfg")
            precio = precio.find_all('span')
            precio = precio[2].text.strip()
            indice = precio.find('Price')
            precioFinal= precio[indice:]
            precioFinal = precioFinal[6:]
        except:
            pass      
        

        listaInformacion = informacionOficial(URL)
        piezas = listaInformacion[0]
        enlaceProducto =listaInformacion[1]

        identificador = identificador.text.strip()
        nombre = nombre.text.strip()
        if (len(identificador)>=10):            
            identificador = identificador.split('.')
            identificador = identificador[0]

        #print(identificador, nombre, enlaceProducto,categoria,precioFinal,piezas)
        listaGeneral.append((identificador, nombre, enlaceProducto,categoria,precioFinal,piezas ))
    
    
    lista_paginas = parser.find('nav', class_='Paginationstyles__PagesNav-npbsev-2 hYNPJr')
    if str(type(lista_paginas)) == "<class 'bs4.element.Tag'>":
        paginas = lista_paginas.find_all('a', class_ ='Paginationstyles__NextLink-npbsev-10 ewFiGQ')
        for pagina in paginas:
            listaGeneral.extend(legoOficial(pagina['href']))

    return listaGeneral

if __name__ == "__main__":

    listaCambios = ProductosDjdango.objects.all()
    for articulo in listaCambios:
        articulo.estado = False
        articulo.save()

    tiempo_inicial = time() 
>>>>>>> 7c37c163dfb537f43f55c219269573aee641bf73

    categorias = ['architecture','city','friends','lego-batman-sets','minecraft']
    URLSResto = ['/b/lego/-/N-56h5nZ5chhkZ9imip?type=products&lnk=LEGOArchitectur','/c/lego-city/-/N-k854h?lnk=LEGOCity','/c/lego-friends/-/N-h258a?lnk=LEGOFriends','/c/lego-batman/-/N-4rt2x?lnk=LEGOBatman','/c/lego-minecraft/-/N-p2onl?lnk=LEGOminecraft']
    

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

    categoriasOficial = ['/en-us/themes/architecture','/en-us/themes/city','/en-us/themes/friends','/en-us/themes/lego-batman-sets','/en-us/themes/minecraft']

    poolLego = Pool(cpu_count()*8)

    with poolLego as p:
        listasOficial = p.map(legoOficial,categoriasOficial)
    
    lista_productosOficial=[]
    categoriasOficial=[]
    for elemento in listasOficial:
        for element in elemento:
            lista_productosOficial.append(element)
    
    for productoOficial in lista_productosOficial:
        try:
            prod = ProductosDjdango.objects.get(idProducto = productoOficial[0])
            prod.link2 = productoOficial[2]
            prod.save()
        except:
            prod= ProductosDjdango(idProducto = str(productoOficial[0]), nombre =productoOficial[1], link2 = productoOficial[2], categoria = productoOficial[3], precio = float(productoOficial[4]), nPiezas = productoOficial[5],observaciones = 'aun no disponible', estado =True)
            prod.save()
    

    tiempo_final = time() 
    tiempo_ejecucion = tiempo_final - tiempo_inicial
    
    
    print ('El tiempo de ejecucion fue:') #En segundos
    print(tiempo_ejecucion)

