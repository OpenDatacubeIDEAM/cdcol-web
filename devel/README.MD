# CDCOL Ambiente de Desarrollo Web

Para desplegar el ambiente de desarrollo web, se requiere lo siguiente:

* Sistema Operativo Ubuntu 
* Git
* docker 
* docker-compose

### Preparación del Ambiente de Desarrollo

Abre una terminal en el Sistema Operativo Ubuntu y procede con la instalciónde los siguientes paquetes:

Instalación de Git

```sh 
sudo apt install git
```

Instalación de docker y docker-compose

```sh 
sudo apt install docker.io
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker 
sudo reboot now
sudo apt install docker-compose 
```

Comenta la line **PRODUCTION** en el archivo environment para indicar a la aplicación web que no estamos en producción. **Nota: Cuando termines el desarollo debes volver a descomentar esta linea.**

```sh 
# Uncommend to serve static file with nginx
PRODUCTION='on'

# Uncommend to serve static file with nginx
# PRODUCTION='on'
```

Despliega la base de datos de pruebas

```sh
docker-compose up -d db
```

Despliega el servidor web

```sh
docker-compose up web
```

Agunos cambios en el código requieren que reinicios el servicio web. Puedes reiniciar el servidor usando Ctrol + C (para salir) y volver a ejecutar el comando anterior.

### Acceso a la Aplicación Web

La aplicación web estará disponible en la siguiente URL http://localhost:8001. 