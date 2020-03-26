import django
import os
import requests
from bs4 import BeautifulSoup


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SriwLego.settings")
django.setup()

from recomendador.models import Producto as ProductosDjdango

listaGeneral = []

def informacion(URLP):
    URLProducto = 'https://www.lego.com'
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

def legoOriginal(URL, categoria):
    page = requests.get(URL)
    parser = BeautifulSoup(page.content, 'html.parser')
    lista_productos = parser.find('div', class_='ProductListingsstyles__Content-sc-1taio5c-2 iHRYuT')
    productos = lista_productos.find_all('div', class_='ProductLeafSharedstyles__Wrapper-sc-1epu2xb-0 hIVRQm')

    for producto in   productos:
        URL = producto.find('a', class_= 'ProductImagestyles__ProductImageLink-sc-1sgp7uc-0 hoRfhG')['href']
        nombre = producto.find('h2', class_='ProductLeafSharedstyles__Title-sc-1epu2xb-9 eNbUrI Text__BaseText-aa2o0i-0 zdErV')
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
        

        listaInformacion = informacion(URL)
        piezas = listaInformacion[0]
        enlaceProducto =listaInformacion[1]

        identificador = identificador.text.strip()
        nombre = nombre.text.strip()
        if (len(identificador)>=10):            
            identificador = identificador.split('.')
            identificador = identificador[0]

        listaGeneral.append((identificador, nombre, enlaceProducto,categoria,precioFinal,piezas ))
    
    
    lista_paginas = parser.find('nav', class_='Paginationstyles__PagesNav-npbsev-2 hYNPJr')
    if str(type(lista_paginas)) == "<class 'bs4.element.Tag'>":
        paginas = lista_paginas.find_all('a', class_ ='Paginationstyles__NextLink-npbsev-10 ewFiGQ')
        for pagina in paginas:
            legoOriginal('https://www.lego.com'+pagina['href'],categoria)
          

if __name__ == "__main__":
    
    categorias = ['architecture','city','friends','lego-batman-sets','minecraft']
    for i in categorias:
        URL = 'https://www.lego.com/en-us/themes/'
        URL += i
        legoOriginal(URL,i )
        
    for elemento in listaGeneral:
        try:
            prod = ProductosDjdango.objects.get(idProducto = elemento[0])
            prod.link2 = elemento[2]
            prod.save()
        except:
            prod= ProductosDjdango(idProducto = str(elemento[0]), nombre =elemento[1], link2 = elemento[2], categoria = elemento[3], precio = float(elemento[4]), nPiezas = elemento[5],observaciones = 'aun no disponible', estado =True)
            prod.save()

            

    