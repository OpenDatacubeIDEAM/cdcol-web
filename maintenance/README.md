# CDCOL WEB MAINTENANCE PAGE

## To deply the maintenance web page manually 

1. Copy and paste the static file on this folder.
2. Create a backup of the */etc/nginx/conf.d/default.conf* file.
2. Copy the default.conf file into the */etc/nginx/conf.d/* directory. 

## To deploy the maintenance web page manually with Docker

Copy and paste the static file on this folder. Then perform the following command.

```sh
docker run -it -d --name nginx -v ${PWD}:/var/www/ -v ${PWD}/default.conf:/etc/nginx/conf.d/default.conf nginx 
```