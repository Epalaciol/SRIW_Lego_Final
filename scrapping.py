import requests
from bs4 import BeautifulSoup

def legoOriginal():
    categorias = ['architecture','city','friends','lego-batman-sets','minecraft']
    for i in categorias:
        URL = 'https://www.lego.com/en-us/themes/'
        URL += i
        page = requests.get(URL)
        parser = BeautifulSoup(page.content, 'html.parser')
        lista_productos = parser.find('div', class_='ProductListingsstyles__Content-sc-1taio5c-2 iHRYuT')
        empleos = lista_productos.find_all('div', class_='ProductLeafSharedstyles__Wrapper-sc-1epu2xb-0 hIVRQm')

        for empleo in empleos:
            titulo = empleo.find('span', class_='Markup__StyledMarkup-ar1l9g-0 bTYWAd')
            print(titulo.text.strip())
        print()

if __name__ == "__main__":
    legoOriginal()