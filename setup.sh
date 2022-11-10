#!/bin/bash
# create virtual environment
python -m venv venv_CREMEv2

# active venv
source venv_CREMEv2/bin/activate

# update pip
pip install --upgrade pip

# install libraries
# should check python-interface later
pip install -r requirements.txt

# create database
python manage.py migrate
python manage.py makemigrations CREMEapplication
python manage.py migrate

#chmod -R 775 ./
chmod -R 775 ./CREME_backend_execution/scripts

# create supper user
python manage.py createsuperuser

