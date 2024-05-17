MANAGE = python3 manage.py
ccc:
	ls
#run:
#	$(MANAGE) runserver

m1:
	$(MANAGE) makemigrations

m2:
	$(MANAGE) migrate

superuser:
	$(MANAGE) createsuperuser

worker:
	celery -A config worker -l info

dumpdata:
	$(MANAGE) dumpdata > db.json


extensions-install:
	poetry add django-extensions
	poetry add ipython
	# 'django_extensions'                                | add to the INSTALLED_APPS in settings.py

fix:
	$(MANAGE) reset_db --noinput
	$(MANAGE) migrate
	rm -rf ./media/*
	$(MANAGE) init_script
	$(MANAGE) runserver

#test-fix:
#	$(MANAGE) reset_db --noinput --database=test
#	$(MANAGE) migrate --database=test
##	rm -rf ./media/*
#	$(MANAGE) init_script --database=test
#	$(MANAGE) runserver
down:
	sudo docker compose down -v

up:
	sudo docker-compose up

up+:
	sudo docker-compose up --build

prune:
	sudo docker system prune -a --volumes --force
startapp:
	$(MANAGE) migrate --no-input
	$(MANAGE) loaddata db.json
	$(MANAGE) collectstatic --no-input
	gunicorn GoldBoost.wsgi:application --bind 0.0.0.0:8000

create_app_example:
	$(MANAGE) startapp website ./src/website/


locale_cmd_1:
	django-admin makemessages -l en
comp_msg:
	django-admin compilemessages

run1:
	$(MANAGE) runserver --settings config.settings.kino_admin 8000

run2:
	$(MANAGE) runserver --settings config.settings.kino_cms 7000