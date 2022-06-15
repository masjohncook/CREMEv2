#!/bin/bash
#install redis
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make
cd -

# create virtual environment
python -m venv venv_CREME-N

# active venv
source venv_CREME-N/bin/activate

# update pip
pip install --upgrade pip

# install libraries
pip install -r requirements.txt

# create database
python manage.py migrate
python manage.py makemigrations CREMEapplication
python manage.py migrate

#chmod -R 775 ./
chmod -R 775 ./CREME_backend_execution/scripts

# create supper user
python manage.py createsuperuser

