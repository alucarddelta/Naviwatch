# API Skeleton Example

A basic API example that includes routes for GET, PUT, DELETE, and POST

## Key libraries

- Flask==1.0.2
- flask-accept==0.0.6
- Flask-Cors==3.0.7
- flask-marshmallow==0.10.1
- Flask-SQLAlchemy==2.4.0
- marshmallow==2.19.2
- SQLAlchemy==1.3.3
- alembic==1.0.10
- pymysql==0.9.3


## Setup
Create a virtual environment and install the necessary packages
```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```
Open a MySQL console session with your MySQL server and enter the following (replace details as appropriate):
```
CREATE USER 'someusername'@'localhost' IDENTIFIED BY 'somepassword';
CREATE DATABASE somedatabase;
GRANT ALL PRIVILEGES ON somedatabase.* TO 'someusername'@'localhost' WITH GRANT OPTION;
```

Copy config.template.py to config.py and modify values as appropriate:

```
cp config.template.py config.py
```

Edit alembic.ini and adjust sqlalchemy.url as appropriate

Run alembic upgrade

```
alembic upgrade 9c37c254a0e9
```
Edit run.sh and then start the application (production)
```
./run.sh
```
run dev.py to start the application (dev) - make sure your venv is active
```
python3 dev.py
```

## How to add data models
- Create a new class in models.py that inherits from Base
- create and apply an Alembic migration:

```
alembic revision --autogenerate
alembic upgrade <revision number>
```

## Todo
- flask swagger
- complete docstrings and sphinx how-to
- example routes for celery interaction
- model relationships