#!/bin/bash

pip install -r requirements.txt

source environment

python manage.py makemigrations --noinput --merge

python manage.py migrate --noinput

python manage.py runserver 0.0.0.0:8000