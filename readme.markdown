# README #

A continuación se presentan los pasos para el despliegue del proyecto CDCol
<!-- 
https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04
http://michal.karzynski.pl/blog/2013/06/09/django-nginx-gunicorn-virtualenv-supervisor/
http://docs.gunicorn.org/en/stable/run.html
 -->

# Instalación de dependencias

Se instalarán las siguientes aplicaciones:

* python
* postgresql
* nginx

Para esto se ejecuta los siguientes comandos en Ubuntu

    sudo apt-get update
    sudo apt-get install python-pip python-dev libpq-dev postgresql postgresql-contrib nginx virtualenv

# Configuración de Ambiente Virtual

Se debe instalar el paquete virtualenv en el directorio donde va a quedar el proyecto

```
#!python
pip install virtualenv
# o también es posible instalarlo mediante el sistema operativo
sudo apt-get install virtualenv
# Se crea el entorno virtual
virtualenv v_ideam
# Para ingresar al ambiente se puede utilizar . bin/activate ó source bin/activate ingresando a la carpeta v_ideam
# Crear directorio donde se va a instalar al aplicación
mkdir projects
```

## Descargar el proyecto

Se deberá descargar la aplicación mediante el repositorio de git

    # se ingresa a la carpeta de los proyectos
    cd projects
    # se clona el repositorio
    git clone https://Manre@bitbucket.org/ideam20162/web-app.git


## Instalación de PostgresSQL

Se deberá instalar PostgreSQL, en Ubuntu el comando sería el siguiente.

```
#!bash
sudo apt-get install postgresql postgresql-contrib
```

**Nota**: Se debe tener en cuenta que antes de ejecutar el comando anterior se deben actualizar el respositorio ya que es posible que se instale una versión anterior.

## Configuración de Postgres

Se deberá crear la base de datos donde se almacenará la información de la web.

    # usuario postgres
    sudo su - postgres
    # ingreso a psql
    psql
    # se crea la base de datos
    CREATE DATABASE ideam;
    # se ingresa a la base de datos
    \c ideam
    # se crea usuario en la base de datos
    CREATE USER cdcol_web with password 'CDCol_web_2016' ;
    # Configurar postgres para recibir trafico externo
    sudo nano pg_hba.conf
    # IPv4 local connections:
    host    all             all             192.168.106.0/25            md5
    sudo nano postgresql.conf
    # cambiar parámetro para escuchar ips
    listen_addresses = '*'

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
export IDEAM_DATABASE_URL=""
export IDEAM_PRODUCTION_DATABASE_URL=""
export IDEAM_API_URL=""
export IDEAM_SENDGRID_USERNAME=""
export IDEAM_SENDGRID_PASSWORD=""
```

## Despliegue de prueba

Para probar el despliegue sólo es necesario ejecutar el siguiente comando

```
#!python
# Realizar migraciones
python manage migrate
# Utilizando el puerto por defecto
python manage.py runserver
# Utilizando el puerto 8000
python manage.py runserver 0.0.0.0:8000
# Creando el superusuario
python manage.py createsuperuser
# usuario: superadminuser
# email: cuboimagenes@ideam.gov.co
# password: %Pass_18_Cubo%
# 
# 
```






















# Configuración Gunicorn como servicio

Se deberá crear un archivo de servicio, para esto.

    sudo nano /etc/systemd/system/gunicorn.service

En este archivo especificaremos la siguiente configuración.

    [Unit]
    Description=gunicorn daemon
    After=network.target

    [Service]
    User=ideam
    Group=www-data
    WorkingDirectory=/home/ideam/Documents/code/v_ideam/projects/ideam_cdc
    ExecStart=/home/ideam/Documents/code/v_ideam/bin/gunicorn --workers 3 --bind unix:/home/ideam/Documents/code/v_ideam/projects/ideam_cdc/ideam.sock ideam_cdc.wsgi:application

    [Install]
    WantedBy=multi-user.target

A continuación guardaremos el servicio y procederemos a iniciar el servicio de Gunicorn.

    sudo systemctl start gunicorn
    sudo systemctl enable gunicorn

# Configuración Nginx

Se deberá crear un archivo el cual contendrá la información relevante al proyecto, para esto.

    sudo nano /etc/nginx/sites-available/ideam
    # en este archivo se agregará la siguiente configuración
    server {
        listen 80;
        server_name 172.24.99.167;

        location = /favicon.ico { access_log off; log_not_found off; }
        location /static/ {
            root /home/ideam/Documents/code/v_ideam/projects/ideam_cdc/ideam_cdc/static_dirs/;
        }

        location / {
            include proxy_params;
            proxy_pass http://unix://home/ideam/Documents/code/v_ideam/projects/ideam_cdc/ideam.sock;
        }
    }

Ahora se procede a crear hardlink

    sudo ln -s /etc/nginx/sites-available/ideam /etc/nginx/sites-enabled

Para revisar que la configuración se encuentra correcta se puede ejecutar el comando

    sudo nginx -t

Ahora se procederá a reiniciar el servicio de nginx con el siguiente comando

    sudo systemctl restart nginx

Si existen inconvenientes se deberá revisar el archivo

    sudo tail -f /var/log/nginx/error.log

Si existen problemas de permisos para el archivo .sock se podrán corregir con los siguientes comandos:

    chgrp ideam ideam.sock && chmod g+rw ideam.sock
    chmod +x /home/ideam /home/ideam/Documents/code/v_ideam/projects/ideam_cdc
    chmod g+s /home/ideam/Documents/code/v_ideam/projects/ideam_cdc




Se deberá ejecutar el siguiente comando en la consola del SO utilizado.
# Configuración de nginx

Dependiendo del SO utilizado, se deberá editar el archivo de configuración si se desea cambiar el puerto por el que se va a escuchar.

    nano /usr/local/etc/nginx/nginx.conf
    ...
    server{
        listen      80    # cambiar por el puerto deseado
    ...









-----------
## Procedimiento para actualizar el código






## Versiones Utilizadas

Se utilizaron las siguientes versiones para el portal.

* PostgreSQL, Version 9.5.4.2 (9.5.4.2)