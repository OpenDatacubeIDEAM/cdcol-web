# README #

A continuación se presentan los pasos para el despliegue del proyecto CDCol
<!-- 
https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04
http://michal.karzynski.pl/blog/2013/06/09/django-nginx-gunicorn-virtualenv-supervisor/
http://docs.gunicorn.org/en/stable/run.html
 -->


# nginx

## Instalación de nginx

Se deberá ejecutar el siguiente comando en la consola del SO utilizado.

    # OSX
    brew install nginx

# Configuración de nginx

Dependiendo del SO utilizado, se deberá editar el archivo de configuración si se desea cambiar el puerto por el que se va a escuchar.

    nano /usr/local/etc/nginx/nginx.conf
    ...
    server{
        listen      80    # cambiar por el puerto deseado
    ...

## Configuración Ambiente virtual

Se debe instalar el paquete virtualenv en el directorio donde va a quedar el proyecto

```
#!python
pip install virtualenv
# Se crea el entorno virtual
virtualenv v_ideam
# Para ingresar al ambiente se puede utilizar . bin/activate ó source bin/activate ingresando a la carpeta v_ideam
```

## Instalación de PostgresSQL

Se deberá instalar PostgreSQL, en Ubuntu el comando sería el siguiente.

```
#!bash
sudo apt-get install postgresql postgresql-contrib
```

**Nota**: Se debe tener en cuenta que antes de ejecutar el comando anterior se deben actualizar el respositorio ya que es posible que se instale una versión anterior.


## Instalación de dependencias

Se deben instalar todas las dependencias para que la aplicación pueda ejecutarse sin inconvenientes.

```
#!python
pip install -r /path/requirements.txt
```

**Nota**: Si al instalar el paquete psycopg2 existen inconvenientes con la ruta se debe exportar una variable de entorno.

```
#!python
export PATH=/Applications/Postgres.app/Contents/Versions/9.5/bin:"$PATH"
```

## Configuración de variables de entorno

Se deberán configurar las siguientes variables de entorno, este archivo dependerá del SO utilizado.

```
#!bash
# Buscar el archivo .bash_profile/.bash_rc
cd
nano .bash_profile
# Adicionar las siguientes lineas dentro del archivo
export IDEAM_STORAGE_UNIT_DIRECTORY_PATH="..."
export IDEAM_SENDGRID_USERNAME="..."
export IDEAM_SENDGRID_PASSWORD="..."
export IDEAM_PRODUCTION_DATABASE_URL="..."
export IDEAM_DATABASE_URL="..."
```

## Despliegue de prueba

Para probar el despliegue sólo es necesario ejecutar el siguiente comando

```
#!python
# Utilizando el puerto por defecto
python manage.py runserver
# Utilizando el puerto 8000
python manage.py runserver 0.0.0.0:8000
```

## Versiones Utilizadas

Se utilizaron las siguientes versiones para el portal.

* PostgreSQL, Version 9.5.4.2 (9.5.4.2)