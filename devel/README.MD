# CDCOL WEB DEVELOPMENT WITH DOCKER

To deploy this development environmet you require the following to be installed:

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