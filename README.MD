# CDCOL WEB SERVER

## Development

If you use docker you need to get installed in your computer the following:

* docker 
* docker-compose

Then look at the **devel folder**, you will be able to deploy a containerized development
environmet for this web application.

Deploy the test database:

```sh
docker-compose up -d web_db
```

Deploy the test web server:

```sh
docker-compose up web
```

Some changes to the web source code required you to restart, you can close the web using Ctrl + C and perform the command above to start your web server again.

You are ready do develop in your computer, the application will be available at http://localhost:8001. 
You can improve the *docker-compose.yml* file in the devel folder to add more services.

### Database backup

To perform a backup of some database model, perform the following command. Change **auth.group** for the app.model_name and **.1group.json** for a name of your preference.

Source the env variables.

```sh
export $(egrep -v '^#' environment | xargs)
```

Create database model data backup in json format.

```sh
python3.6 manage.py dumpdata --natural-foreign --natural-primary --indent 2 auth.group > data/1.group.json
```

## Production 

The instalation script can be founded [here](https://gitlab.virtual.uniandes.edu.co/datacube-ideam/scripts-despliegue-desacoplado/blob/open_data_cube/web_install.sh).

# NGINX 

Please check this section of the configuration file match the configuration file installed 
by the web instalation script 

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