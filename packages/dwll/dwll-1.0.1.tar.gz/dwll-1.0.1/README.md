# DWLL
## _Django Web Launch Library_

Django Web Launch Library es una librería de elementos utilitarios que le permitirán generar aplicaciones Web (Backend-Frontend) bajo framework Django, de forma rápida y sencilla, asi evitaremos la construcción de elementos habituales en la mayoria de sistemas Web, y aceleraremos el desarrollo de su aplicación. DWLL contiene elementos que cubre los siguientes módulos:

- Vistas
- Formularios
- Modelos
- Mensajes y Traducciones
- Configuración
- URLs
- Login

## Características

- Modelos y Mixins base para auditar modelos, filtros de activos y permitir soft-delete
- Vistas virtuales que permiten crear vistas de formato CRUD con muy pocas lineas de codigo
- Sistema de mensajes de texto a ser usados en todo el sitio Web y en el backend, con su respectiva administración de textos por lenguaje para la gestión de su traducción.
- Sistema de configuraciones para agregar banderas y propiedades administrables a su aplicación Web.
- Autogenerador de una apĺicación (plantilla) principal que le permitirán arrancar el desarrollo rápidamente.

DWLL permite que los desarrolladores tomen un camino claro y directo en la construcción de sus aplicaciones, siguiendo el principio DRY, Don't Repeat Yourself:
Como [Joaquin Medina] escribe en [su Blog][df1]

> DRY, es una filosofía de definición de procesos que 
> promueve la reducción de la duplicación especialmente 
> en programación. Según este principio toda pieza de 
> información nunca debería ser duplicada debido a que 
> la duplicación incrementa la dificultad en los cambios 
> y evolución posterior, puede perjudicar la claridad 
> y crear un espacio para posibles inconsistencias

Esta librería permitirá evitar que rescriba los elementos más comunes en el desarrollo de aplicaciones Web. Proporciona un camino definido a seguir, y con la menor cantidad de código posible.

## Tecnología

DWLL esta dirigido al desarrollo de aplicaciones Web con Django 4.0 y hace uso de las siguientes librerías:

- [Allauth] - Librería para Django que permite el manejo de todo lo relacionado con la autenticación y registro de usuarios.
- [Beautifulsoup4] - Librería que permite el manejo de archivos html usados por el autogenerador de DWLL
- [Locust] - Librería que permite realizar pruebas, de estress y de carga, a las pantallas de las aplicaciones autogeneradas con DWLL

## Instalación

DWLL requiere [Django](https://docs.djangoproject.com/en/4.0/releases/4.0/) v4.0+ para funcionar.

1. Instale un entorno virtual para instalar Django y DWLL.

```sh
sudo apt-get install python3-pip
sudo pip3 install virtualenv 
virtualenv -p python3 venv
source venv/bin/activate
```

2. Instale Django, dependencias, y DWLL

```sh
pip install django django-allauth locust beautifulsoup4
pip install dwll
```

3. Cree un proyecto Django, en este ejemplo llamaremos a este proyecto (o el nombre que usted quiera): "myproject"

```
django-admin startproject myproject
cd myproject
```

4. Incluir las siguientes aplicaciones en INSTALLED_APPS de su archivo myproject/myproject/settings.py:

```
'allauth',
'allauth.account',
'allauth.socialaccount',
'dwll',
```

5. Ejecute el generador de su primera aplicación...

```
./manage.py dwll-gen
```

...y siga las instrucciones indicadas en la consola. Puede elegir generar la plantilla de una aplicación con un modelo de ejemplo, o solamente la estructura base de una aplicación para iniciar. En este ejemplo llamaremos a la aplicacion "myapp" y al modelo "mymodel" (El nombre de la aplicación, y el modelo, puede ser el que usted quiera).

Al ejecutar la consola, además, se agregarán lineas de código, a su archivo de settings.py y urls.py, que permiten que la nueva aplicación pueda ejecutarse en página de inicio.

**Nota:** Luego puede formatear el código autogenerado a discreción.

6. Una vez generado el proyecto, realizaremos la migracion a la base de datos, esto solo deberá realizarlo si ha seleccionado generar el modelo de ejemplo, caso contrario omita la primera linea del siguiente comando:

```
./manage.py makemigrations myapp
./manage.py migrate
```

Al ejecutar lo anterior, deberia conseguir una salida similar a la siguiente (y adicionalmente un listado de todos los modelos migrados a su base de datos temporal):

```
Migrations for 'myapp':
  myapp/migrations/0001_initial.py
    - Create model MyModel
```

7. Ahora es necesario crear un super usuario para probar la aplicación y la administración del sistema.
```
./manage.py createsuperuser
```

Deberá seguir las instrucciones en consola. Puede ingresar el nombre, email y clave que prefiera, pero deberá recordarlos para poder usar esos datos luego.

8. Finalmente, ejecutaremos el proyecto con el siguiente comando:
```
./manage.py runserver
```

9. Podremos ingresar a la siguiente URL para ver nuestro nuevo home-page http://localhost:8000. Además, si ha seleccionado generar un modelo de ejemplo, podrá revisar un ejemplo del CRUD autogenerado para dicho modelo en la siguiente dirección: http://localhost:8000/mymodels/ (para acceder deberá autenticarse con su usuario generado, o con cualquier usuario registrado en la consola administrativa de Django: http://localhost:8000/admin)

## Pruebas
DWLL autogenera dos archivos que permiten al desarrollador probar la funcionalidad y eficiencia de su nueva aplicación.

### Funcionalidad
Para probar la funcionalidad de una algoritmo o un segmento de su codigo ejecute el siguiente comando>
```
./manage.py test myapp
```

### Estress y Carga
Para realizar pruebas de carga y estress a sus pantallas, ejecute los siguientes comandos:
```
cd myapp
locust
```
Esto inicia el servidor de Locust para pruebas de carga y estress. Para iniciar la preparación y ejecución de las pruebas simplemente ingrese a la siguiente dirección: http://localhost:8089/, alli podrá ejecutar cualquier clase de prueba con varios usuarios recurrentes a la vez y medir el rendimiento de su aplicación Web, aún luego de incluir mayor funcionalidad que la autogenerada.

## Licencia

MIT, UIsrael

**Free Software, Hell Yeah!**

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [Allauth]: <https://django-allauth.readthedocs.io/en/latest/overview.html>
   [Beautifulsoup4]: <https://pypi.org/project/beautifulsoup4/>
   [dwll]: <https://github.com/jimuisrael/dwll>
   [df1]: <http://joaquin.medina.name/web2008/documentos/informatica/documentacion/logica/OOP/Principios/2012_07_30_OopNoTeRepitas.html>
   [Locust]: <https://locust.io/>
   
