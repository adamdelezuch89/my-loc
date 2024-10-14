
# Run commands in docker:
## any
docker-compose run --rm app sh -c ""
## lint and tests
docker compose run --rm app sh -c "python manage.py wait_for_db && python manage.py test"
docker compose run --rm app sh -c "cd app && flake8"
## new project
docker compose run --rm app sh -c "django-admin startproject app ."
## new app
docker compose run --rm app sh -c "python manage.py startapp core"

# VENV
## create
* python -m venv venv
* pip install -r requirements.txt 
## use
* source ./venv/bin/activate
* deactivate