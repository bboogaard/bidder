#!/bin/bash

python manage.py migrate --settings=app.settings-docker
python manage.py collectstatic --no-input --settings=app.settings-docker