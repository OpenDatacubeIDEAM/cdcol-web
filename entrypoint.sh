#!/bin/bash

pip install -r requirements.txt

source environment

python manage.py makemigrations --noinput --merge

python manage.py migrate --noinput

# Load backup data
python manage.py loaddata admin.json
python manage.py loaddata group.json

python manage.py runserver 0.0.0.0:8000