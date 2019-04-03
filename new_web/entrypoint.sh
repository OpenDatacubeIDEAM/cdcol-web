#!/bin/bash

# Install new rewuirements
pip install -r requirements.txt
# Source env variables
source environment
# Create migrations 
python manage.py makemigrations --noinput --merge
# Migrations 
python manage.py migrate --noinput
# Load backup data
# python manage.py loaddata database.json
# Running development server
python manage.py runserver 0.0.0.0:8000