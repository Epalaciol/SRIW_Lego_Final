import requests
from bs4 import BeautifulSoup

def informacion(URLP):
    URLProducto = 'https://www.lego.com'
    URLProducto += URLP
    pagina = requests.get(URLProducto)
    parser = BeautifulSoup(pagina.content, 'html.parser')
    listarPrecios = parser.find('div', class_ = 'ProductPricestyles__Wrapper-vmt0i4-1 bEUKjC')
    listarTitulo = parser.find('h1', class_ = 'ProductOverviewstyles__NameText-sc-1a1az6h-2 cZIodu Text__BaseText-aa2o0i-0 lDuRH')
    listarPiezas = parser.find_all('div', class_='ProductDetailsstyles__ProductAttribute-sc-16lgx7x-2 vcPOs')
    piezas  = listarPiezas[1].find_all('span')
    identificador = listarPiezas[3].find_all('span')
    titulo = listarTitulo.find_all('span')

    if str(type(listarPrecios)) == "<class 'NoneType'>":
        precio = 0
    else:
        precio = listarPrecios.text.strip()
        precio= precio[6:]

    titulo = titulo[0].text.strip()
    piezas = piezas[1]
    piezas = piezas.text.strip()
    identificador = identificador[3]
    identificador = identificador.text.strip()
    print(identificador,' ',titulo,' ',piezas, ' ',precio)

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