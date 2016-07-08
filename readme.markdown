# README #

A continuación se presentan los pasos para configurar el proyecto.

##Configuración Ambiente virtual

Se debe instalar el paquete virtualenv en el directorio donde va a quedar el proyecto

```
#!python
pip install virtualenv
# Se crea el entorno virtual
virtualenv v_ideam
```

## Instalación de dependencias

Se deben instalar todas las dependencias para que la aplicación pueda ejecutarse sin inconvenientes.

```
#!python
pip install -r /path/requirements.txt
```

**Nota**: Si al instalar el paquete psycopg2 existen inconvenientes con la ruta se debe exportar una variable de entorno.

```
#!python
export PATH=/Applications/Postgres.app/Contents/Versions/9.4/bin:"$PATH"
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