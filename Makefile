VENV = $(HOME)/.virtualenvs/django_ecommerce/bin

lint:
	$(VENV)/isort .;
	$(VENV)/black .;
	$(VENV)/isort;

server:
	$(VENV)/python src/manage.py runserver
