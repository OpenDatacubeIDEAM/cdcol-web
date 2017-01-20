#!/bin/bash

DJANGO_VIRTUALENV=$HOME/Documents/code/v_ideam


echo "$(date) RUNNING NOTIFICATION MONITOR"
cd $DJANGO_VIRTUALENV
source bin/activate
python projects/ideam_cdc/ideam_notifier.py
echo "$(date) DONE"
