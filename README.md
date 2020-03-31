# SRIW-Recomendador
Sistema de recomendacion de Legos


Para su instalancion es necesario el uso de:
- Python 3.7 o superior
- Django 3.0.4
- suprise
- selenium
- pandas
- bs4 (beautifulsoup)

Para iniciar el programa se debe ejecutar la consola de comandos en la carpeta SriwLego, y posteriormente ejecutar el comando "python manage.py runserver";
Luego dirigirse a la direccion proporcionada y iniciar o registrarse.

## WebScrapping
### Pagina Oficial Lego
Para este web scrapping utilizamos la tecnica aprendida en clase con la libreria bs4 para obtener el codigo html de las paginas web que se querian consultar; se buscaron los links de las categorias pedidas en el trabajo 2  y se dispuso a buscar el link; al haber obtenido todo el contenido de la pagina  se empiezan a buscar la etiquetas en HTML donde estan guardados los valores que necesitamos. 
Para la paginación se busco una etiqueta que al analizar las paginas miraba si habian mas y se obtenian los links (href) y se envian recursivamente en la misma función. La mayoria de items obtenidos se encontraban al cargar la categoria pero para saber las piezas se debia ir directamente al link del producto  por lo cual se diseño otra función  que analizara la pagina del producto y extraer las piezas

### Pagina Target
Para extraer la información en esta pagina se utilizo exactamente lo mismo descrito para la pagina oficial Lego pero esta vez  como la pagina cargaba los archivos renderizando con javascript se utilizo la libreria selenium para poder obtener todos los articulos de la pagina. La función del selenium que se implemento mediante el uso del navegador Firefox y consiste en hacer que el programa haga scroll hasta que todos lo productos esten cargados en el pagina y asi se pueda extraer la información de esta pagina.

## Cold Star Problem
Para solucionar este problema se implemento un formulario  en el que se le hacen unas preguntas al usuario  para poder dar unas recomendaciones iniciales en base a las respuestas; estas recomendaciones se hacen al principio mientras el usuario empieza a interactuar con la pagina. Despues de que el usuario interactue con la pagina se hace un perfil con el cual se pueden hacer recomendaciones con base a los  gustos demostrados por la persona en la intercción con la pagina web
