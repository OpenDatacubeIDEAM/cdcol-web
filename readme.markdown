# README #

A continuación se presentan los pasos para el despliegue del proyecto CDCol

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
export IDEAM_PRODUCTION_DATABASE_URL="postgres://cdcol_web:CDCol_web_2016@localhost/ideam"
export IDEAM_API_URL="http://192.168.106.10:8000"
export IDEAM_MAIL_HOST="mail.ideam.gov.co"
export IDEAM_MAIL_USER="cuboimagenes@ideam.gov.co"
export IDEAM_MAIL_PASSWORD="15CuboSatelite20"
export IDEAM_MAIL_PORT="25"
export IDEAM_DC_STORAGE_PATH="/dc_storage"
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
# Archivos estaticos
python manage.py collectstatic
# Creando el superusuario
python manage.py createsuperuser
# usuario: superadminuser
# email: cuboimagenes@ideam.gov.co
# password: %Pass_18_Cubo%
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
    User=cubo
    Group=cubo
    WorkingDirectory=/home/cubo/Documents/code/v_ideam/projects/ideam_cdc
    EnvironmentFile=/home/cubo/.ideam.env
    ExecStart=/home/cubo/Documents/code/v_ideam/bin/gunicorn --bind 0.0.0.0:8080 ideam_cdc.wsgi:application

    [Install]
    WantedBy=multi-user.target

También se deberá crear archivo el cual contendrá las variables de entorno para esto.

    pwd
    /home/cubo
    nano .ideam.env
    # se adicionaran las siguientes lineas
    IDEAM_PRODUCTION_DATABASE_URL="postgres://cdcol_web:CDCol_web_2016@localhost/ideam"
    IDEAM_API_URL="http://192.168.106.10:8000"
    IDEAM_MAIL_HOST="mail.ideam.gov.co"
    IDEAM_MAIL_USER="cuboimagenes@ideam.gov.co"
    IDEAM_MAIL_PASSWORD="15CuboSatelite20"
    IDEAM_MAIL_PORT="25"
    IDEAM_DC_STORAGE_PATH="/dc_storage"

A continuación guardaremos el servicio y procederemos a iniciar el servicio de Gunicorn.

    sudo systemctl start gunicorn
    sudo systemctl enable gunicorn
    # es posible que sea necesario actualizar los servicios, para esto
    systemctl daemon-reload

# Configuración Nginx

Se deberá crear un archivo el cual contendrá la información relevante al proyecto, para esto.

    sudo nano /etc/nginx/sites-available/ideam
    # en este archivo se agregará la siguiente configuración
    server {
      listen 80;

      location /web_storage {
        alias /web_storage;
      }

      location / {
        proxy_pass http://127.0.0.1:8080;
      }
    }

Se procede a crear hardlink

    sudo ln -s /etc/nginx/sites-available/ideam /etc/nginx/sites-enabled/

Para revisar que la configuración se encuentra correcta se puede ejecutar el comando

    sudo nginx -t

Ahora se procederá a reiniciar el servicio de nginx con el siguiente comando

    sudo systemctl restart nginx

Si existen inconvenientes se deberá revisar el archivo

    sudo tail -f /var/log/nginx/error.log

-----------
# Procedimiento para actualizar el código

En caso de necesitar realizar actualización del código, solo es necesario seguir los siguientes pasos.

    # ingresar a la ruta del ambiente
    cd Documents/code/v_ideam/
    # activar el ambiente virtual
    . bin/activate # o source bin/activate
    # ingresar a la carpeta del proyecto
    cd projects/ideam_cdc/
    # obtener los nuevos cambios desde el repositorio
    git pull
    # en caso de necesitar migraciones recordar que se debe ejecutar
    python manage.py migrate
    # es posible que se necesite reiniciar servicios
    sudo systemctl restart gunicorn
    sudo systemctl restart nginx

# Configuración del sitio

Se deberán realizar los siguientes procedimientos manuales en caso de instalar la aplicación desde cero.

1. Cambio de nombre. Se deberá ingresar al portal de administración a aplicación "sitios" en esta se podrá cambiar el nombre de dominio y nombre a mostrar de al aplicación. Esto se visualizará en el correo.
2. Creación de Topics. Se deberán crear los topics en la aplicación "Topic".

## Versiones Utilizadas

Se utilizaron las siguientes versiones para el portal.

* PostgreSQL, Version 9.5.4.2 (9.5.4.2)