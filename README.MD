# Cubo de Datos de Colombia Aplicación Web

Cubo de datos de Colombia se encuentra disponible en el siguinete link [http://cdcol.ideam.gov.co/](http://cdcol.ideam.gov.co/)

## Módulos de la Aplicación Web

* algorithm: Contiene todo el código fuente y HTML del módulo de Algoritmos. Comprende Temáticas, Algoritmos, Versiones, Parámetros de una Versión.
* execution: Contiene todo el código fuente y HTML del módulo de Ejecuciones de la WEB. Comprende Ejecuciones y Parámetros de una Ejecución.
index: Contiene todo el código fuente y HTML necesario para la visualización del index para cada rol de usuario, Analista, Desarrollador, Administrador de Datos y Analista de Workflows.
* ingest: Contiene todo el código fuente y HTML del módulo de Ingesta. Comprende las Tareas de Ingesta.
* storage: Contiene todo el código fuente y HTML del módulo de Unidades de Almacenamiento.
* template: Contiene todo el código fuente y HTML del módulo de Plantillas (YAML descripción e ingesta y Scripts de generación de metadatos)
* user_profile: Contiene todo el código fuente y HTML para administrar información del perfil de usuario . 
* ideam: Contiene archivos de configuración de toda la aplicación WEB.
* static: Contiene todos los archivos Javascript de la aplicación. 
* templates: Contiene código HTML base de la aplicación WEB.

Otros módulos

* maintenance: contine un conetendor que permite desplegar una venatana de mantenimiento.
* data: mantiene datos para inilizalizar la base de datos (usar solo en desarollo).
* devel: mantiene un mini ambiente de desarrollo para la web.

## Desarollo

Ingresa al directorio *devel* donde encontraras los pasos para desplegar el ambiente de desarrollo para la web.

## Production 

El script de instalación se encuentra en el siguiente [link](https://gitlab.virtual.uniandes.edu.co/datacube-ideam/scripts-despliegue-desacoplado/blob/open_data_cube/web_install.sh).

**IMPORTANTE:** Luego de llevar a cabo al instalación de la aplicación web debe modificar el archivo *environment* con el fin de ajustar parámetros de configuración requeridos por la aplicación.
Los siguientes parámetros son requeridos para evitar fallas en la aplicación cuando intente enviar correos (cuando se envia a revisión un workflows y otros esscenarios).

```sh
WEB_EMAIL_HOST_USER=""
WEB_EMAIL_HOST_PASSWORD=""

```

## Consideraciones en Producción

* NGINX 

Verifica que el archivo de configración de nginx provisto por el script de instalación de la web sea parecido al siguiente: 

```
  # redirect requests to the web server
  location / {
    proxy_read_timeout 36000;
    client_max_body_size 500M;

    # Django allouth use this setting to set all 
    # host urls for account activation and verification
    proxy_set_header Host cdcol.ideam.gov.co;

    # Set this variable with the Web server IP
    proxy_pass http://web:8000;
  }
```