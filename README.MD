## Production

Create a user name **cubo**

```sh
sudo adduser cubo
sudo usermod -aG sudo cubo
su cubo
cd
```

Create a RSA key pair

```sh
ssh-keygen -t rsa -C "usuario_gitlab@ejemplo.edu.co" -b 4096
```

Copy and paste the public key content in **gitlab.virtual.uniandes.edu.co key registration form**.

```sh
cat ~/.ssh/id_rsa.pub
```

Install git

```sh
sudo apt-get install git
```

Pull from git the **web instalation script**.

```sh
git clone git@gitlab.virtual.uniandes.edu.co:datacube-ideam/scripts-despliegue-desacoplado.git --branch open_data_cube
mv scripts-despliegue-desacoplado/web_install.sh $HOME
rm -rf scripts-despliegue-desacoplado
```

Run the instalation script

```sh
bash web_install.sh
```

Check the gunicorn and nginx services 

```sh
sudo systemctl status gunicorn.service
sudo systemctl status nginx.service
```

If one or both service failed, restart them 

```sh
sudo systemctl restart gunicorn.service
sudo systemctl restart nginx.service
```

**IMPORTANT:** For every change you perform over the web application or database, please restart both services.

Check that **environmet** file is configured as you expected. 

## Development

Create a database test database with docker using the following command

```sh
docker run \
	--name web_db \
	-e POSTGRES_USER=cdcol \
	-e POSTGRES_DB=cdcol \
	-e POSTGRES_PASSWORD=cdcol \
	-d postgres
```

Get the container IP Address

```sh
docker inspect web_db | grep IPAddress

            "SecondaryIPAddresses": null,
            "IPAddress": "172.17.0.2",
                    "IPAddress": "172.17.0.2"
```

Add the database and rest api (optional) IP Addresses to your hosts file

```sh
sudo nano /etc/hosts

...
172.17.0.1	api
172.17.0.2	db
...
```

Create a python virtualenv in the project directory, activate the environment and install the application requirements.

```sh
virtualenv --python=python3.6 .env
source .env/bin/activate
pip3.6 install -r requirements.txt
```

Load the environent variables required for the application

```sh
export $(egrep -v '^#' environment | xargs)
```

Create database tables required for the application

```sh
python3.6 manage.py makemigrations
python3.6 manage.py migrate
python3.6 manage.py migrate --run-syncdb
```

Load the initial database data

```sh
python3.6 manage.py loaddata data/1.group.json
python3.6 manage.py loaddata data/2.user.json
python3.6 manage.py loaddata data/3.profile.json
python3.6 manage.py loaddata data/4.topic.json
```

Run the development server

```sh
python3.6 manage.py runserver 0.0.0.0:8000
```

### Database backup

To perform a backup of some database model, perform the following command. Change **auth.group** for the app.model_name and **.1group.json** for a name of your preference.

```sh
python3.6 manage.py dumpdata --natural-foreign --natural-primary --indent 2 auth.group > data/1.group.json
```
