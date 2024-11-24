#!/bin/bash
pip install sqlalchemy
pip install django
django-admin startproject myproject .
python manage.py runserver

#You need give rule for to start sh-file
#chmod +x create-django-project.sh