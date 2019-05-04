#!/bin/bash

# Install new rewuirements
pip install -r requirements.txt
# Source env variables
export $(egrep -v '^#' environment | xargs)

# Setting up database
python3.6 manage.py makemigrations
python3.6 manage.py migrate
python3.6 manage.py migrate --run-syncdb

# Load data 
python3.6 manage.py loaddata data/1.group.json
python3.6 manage.py loaddata data/2.user.json
python3.6 manage.py loaddata data/3.profile.json
python3.6 manage.py loaddata data/4.topic.json

# Run server
python manage.py runserver 0.0.0.0:8000