VENV = $(HOME)/.virtualenvs/django_ecommerce/bin

lint:
	$(VENV)/isort .;
	$(VENV)/black .;
	$(VENV)/flake8;

server:
	sudo systemctl start postgresql.service
	$(VENV)/python src/manage.py runserver

update-database:
	$(VENV)/python src/manage.py makemigrations
	$(VENV)/python src/manage.py migrate
