# Django Pastebin API

## Quick setup

* Create a virtual environment and activate it
  
```shell
virtualenv venv
source venv/bin/activate
```

* Install python dependencies

```shell
pip install -r requirements.txt
```

* Create database and migrations

```shell
python manage.py makemigrations snippets
python manage.py migrate
```

* Start the developmental server
  
```shell
python manage.py runserver
```
