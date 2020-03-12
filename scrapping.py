import requests
from bs4 import BeautifulSoup

def informacion(URLP):
    URLProducto = 'https://www.lego.com'
    URLProducto += URLP
    pagina = requests.get(URLProducto)
    parser = BeautifulSoup(pagina.content, 'html.parser')
    listar = parser.find('span', class_ = 'ProductPricestyles__StyledText-vmt0i4-0 ipNtqe Text__BaseText-aa2o0i-0 bVNVTl')
    if str(type(listar)) == "<class 'NoneType'>":
        precio = 0
    else:
        precio = listar.text.strip()

    print(precio[6:])

def legoOriginal():
    categorias = ['architecture','city','friends','lego-batman-sets','minecraft']
    for i in categorias:
        URL = 'https://www.lego.com/en-us/themes/'
        URL += i
        page = requests.get(URL)
        parser = BeautifulSoup(page.content, 'html.parser')
        lista_productos = parser.find('div', class_='ProductListingsstyles__Content-sc-1taio5c-2 iHRYuT')
        productos = lista_productos.find_all('div', class_='ProductLeafSharedstyles__Wrapper-sc-1epu2xb-0 hIVRQm')

        for producto in   productos:
            URL = producto.find('a', class_= 'ProductImagestyles__ProductImageLink-sc-1sgp7uc-0 hoRfhG')['href']
            informacion(URL)
        
        lista_paginas = parser.find('nav', class_='Paginationstyles__PagesNav-npbsev-2 hYNPJr')
        if str(type(lista_paginas)) == "<class 'bs4.element.Tag'>":
            paginas = lista_paginas.find_all('a', class_ ='Paginationstyles__NextLink-npbsev-10 ewFiGQ')
            for pagina in paginas:
                print(pagina['href'])
        
        print()


if __name__ == "__main__":
    legoOriginal()