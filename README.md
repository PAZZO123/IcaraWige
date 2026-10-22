# IcaraWige

A Django web app where learners join study rooms to discuss programming topics. "Icara wige" means "sit down and learn" in Kinyarwanda.

## Features

- Register, log in and edit a user profile with an avatar
- Create rooms on topics and post messages
- Activity feed of recent messages
- REST API for rooms (Django REST Framework)

## Built with

Python, Django, Django REST Framework, SQLite, HTML and CSS.

## How to run

```bash
cd study
pip install django djangorestframework
python manage.py migrate
python manage.py runserver
```

Then open http://127.0.0.1:8000.
