# README #

El siguiente documento muestra los pasos necesarios para realizar la instalación de la aplicación CDCol.

# Instalación de dependencias

Se instalarán las siguientes aplicaciones.

* python
* postgresql
* nginx
* Virtualenv
* pip
* git

Para esto se ejecutan los siguientes comandos en Ubuntu

    sudo apt-get update
    sudo apt-get install python-pip python-dev libpq-dev postgresql postgresql-contrib nginx virtualenv gunicorn git

# Configuración de Ambiente Virtual

Se debe instalar el paquete virtualenv en el directorio donde va a quedar el proyecto

    pip install virtualenv
    # Se crea el entorno virtual
    virtualenv v_ideam
    # Para ingresar al ambiente se puede utilizar . bin/activate ó source bin/activate ingresando a la carpeta v_ideam
    # Crear directorio donde se va a instalar al aplicación
    mkdir projects

# Descargar el proyecto

Se deberá descargar la aplicación mediante el repositorio de git

    # se ingresa a la carpeta de los proyectos
    cd projects
    # se clona el repositorio
    git clone https://Manre@bitbucket.org/ideam20162/web-app.git


# Instalación de PostgresSQL

En caso de no tener PostgreSQL se deberá realizar la instalación con este comando.

    sudo apt-get install postgresql postgresql-contrib


**Nota**: Se debe tener en cuenta que antes de ejecutar el comando anterior es necesario actualizar el repositorio ya que es posible que se instale una versión anterior. Se recomienda el uso de PostgreSQL Version 9.5.4.2 o superior.

# Configuración de Postgres

Se deberá crear la base de datos donde se almacenará la información de la web. Para esto:

    # usuario postgres
    sudo su - postgres
    # ingreso a psql
    psql
    # se crea la base de datos
    CREATE DATABASE ideam;
    # se ingresa a la base de datos
    \c ideam
    # se crea usuario en la base de datos
    CREATE USER usuario with password 'CDCol_web_2016' ;
    # Configurar postgres para recibir trafico externo
    sudo nano pg_hba.conf
    # IPv4 local connections:
    host    all             all             192.168.106.0/25            md5
    sudo nano postgresql.conf
    # cambiar parámetro para escuchar IPs
    listen_addresses = '*'

## Instalación de dependencias

Se deben instalar todas las dependencias para que la aplicación pueda ejecutarse sin inconvenientes.

    pip install -r /path/requirements.txt

**Nota**: Si al instalar el paquete psycopg2 existen inconvenientes con la ruta se debe exportar una variable de entorno.

    # ejemplo
    export PATH=/Applications/Postgres.app/Contents/Versions/9.5/bin:"$PATH"

# Configuración de variables de entorno

Se deberán configurar las siguientes variables de entorno, recordar que este archivo es posible que dependa del Sistema Operativo utilizado. A continuación se presenta un archivo base el cual debe completarse con los datos de cada variable.

    # Buscar el archivo .bash_profile/.bash_rc
    cd
    nano .bash_profile
    # Adicionar las siguientes lineas dentro del archivo
    export IDEAM_PRODUCTION_DATABASE_URL=""
    export IDEAM_API_URL="http://192.168.106.10:8000"
    export IDEAM_MAIL_HOST=""
    export IDEAM_MAIL_USER=""
    export IDEAM_MAIL_PASSWORD=""
    export IDEAM_MAIL_PORT=""
    export IDEAM_DC_STORAGE_PATH=""
    export IDEAM_WEB_STORAGE_PATH=""

# Despliegue de prueba

Es possible probar ejecutar el ambiente utilizando los siguientes comandos.

    # Realizar migraciones
    python manage.py migrate
    # Utilizando el puerto por defecto
    python manage.py runserver
    # Utilizando el puerto 8000
    python manage.py runserver 0.0.0.0:8000
    # Archivos estaticos
    python manage.py collectstatic
    # Creando el superusuario
    python manage.py createsuperuser

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
    IDEAM_PRODUCTION_DATABASE_URL=""
    IDEAM_API_URL=""
    IDEAM_MAIL_HOST=""
    IDEAM_MAIL_USER=""
    IDEAM_MAIL_PASSWORD=""
    IDEAM_MAIL_PORT=""
    IDEAM_DC_STORAGE_PATH=""
    IDEAM_WEB_STORAGE_PATH=""

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

**Nota**: Se debe tener en cuenta que es necesario montar la carpeta /web_storage y /dc_storage en los directorios que correspondan.

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

1. Cambio de nombre del sitio. Se deberá ingresar al portal de administración a aplicación "sitios" en esta se podrá cambiar el nombre de dominio y nombre a mostrar de la aplicación. Esto se visualizará en el correo.
2. Creación de Topics. Se deberán crear los topics en la aplicación "Topic".

