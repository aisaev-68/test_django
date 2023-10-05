#!/bin/bash
python manage.py makemigrations
python manage.py migrate
#megano python manage.py test tests.test_all
#python manage.py create_groups
python manage.py loaddata tests/fixtures/data-fixtures.json
#python manage.py create_fake
#python manage.py dumpdata product > tests/fixtures/data-fixtures.json
python manage.py runserver 0.0.0.0:8000