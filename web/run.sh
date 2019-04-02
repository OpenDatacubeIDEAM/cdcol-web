#!/bin/bash

DJANGO_VIRTUALENV=$HOME/v_ideam


echo "$(date) RUNNING NOTIFICATION MONITOR"
cd $DJANGO_VIRTUALENV
source bin/activate
python /home/cubo/projects/web-app/ideam_notifier.py
echo "$(date) DONE"
