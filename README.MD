
# Development with docker

The storage module will not work properly because it depends of an API external service.

Create a database

```sh
docker run \
	--name web_db \
	-e POSTGRES_USER=cdcol \
	-e POSTGRES_DB=cdcol \
	-e POSTGRES_PASSWORD=cdcol \
	-d postgres
```

Build the docker image

```sh
docker build -t cdcol_web .
```

Run the conatiner

```sh
docker run -it --name web -v ${PWD}:/usr/src/app --env-file environment --link web_db cdcol_web /bin/bash
```

Install requirements and run the development server

```sh
./entrypoint.sh
```

Exit from container

```sh
exit
```

Start conatiner 

```sh
docker start -ia web
```

Get the container IP to get the web server

```sh
docker inspect  devel_web_1 | grep IPAddress

            "SecondaryIPAddresses": null,
            "IPAddress": "",
                    "IPAddress": "172.20.0.5",
```

Place the ulr http://172.20.0.5:8000/ in the browser.


# Create and Load Database Backups

Create a backup of the Admin user data

```sh
python manage.py dumpdata auth.user --indent 2 > admin.json
```

Load Admin data into the database

```sh
python manage.py loaddata admin.json
```