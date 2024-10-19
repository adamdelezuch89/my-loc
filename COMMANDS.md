
# Run commands in docker:
## any
docker-compose run --rm backend sh -c ""
## lint and tests
docker compose run --rm backend sh -c "python manage.py wait_for_db && python manage.py test"
docker compose run --rm backend sh -c "flake8"
## make migrations
docker compose run --rm backend sh -c "python manage.py makemigrations"
## migrate
docker compose run --rm backend sh -c "python manage.py migrate"
## new project
docker compose run --rm backend sh -c "django-admin startproject app ."
## new app
docker compose run --rm backend sh -c "python manage.py startapp core"
## new superuser
docker compose run --rm backend sh -c "python manage.py createsuperuser"
## console access
docker exec -it <container_name> /bin/sh

# ANGULAR
## new elements
ng generate component <name>
ng generate service <name>
ng generate interface <name>

# VENV
## create
python -m venv venv
pip install -r requirements.txt 
## use
source venv/bin/activate
deactivate

# BASH
## Print frontend file structure
find . -type d -name 'node_modules' -prune -o -type f -print