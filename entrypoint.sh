#!/bin/bash

# Install new rewuirements
pip install -r requirements.txt
# Source env variables
export $(egrep -v '^#' environment | xargs)

# Setting up database
python3.6 manage.py makemigrations --noinput --merge
python3.6 manage.py migrate --noinput
python3.6 manage.py migrate --run-syncdb

# Load data 
python3.6 manage.py loaddata data/1.group.json
python3.6 manage.py loaddata data/2.user.json
python3.6 manage.py loaddata data/3.profile.json
python3.6 manage.py loaddata data/4.topic.json

# Run development server
python manage.py runserver 0.0.0.0:8000

# Run production
# python3.6 manage.py collectstatic --noinput
# gunicorn --timeout 36000 -b 0.0.0.0:8000 ideam.wsgi:application
