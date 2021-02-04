HOST = 0.0.0.0
PORT = 8000

install:
	poetry install

tests: install
	poetry run flake8 . --count --show-source --statistics --max-line-length=88 --extend-ignore=E203
	poetry run black . --check
	poetry run isort . --profile=black
	poetry run pytest --cov=./ --cov-report=xml

export:
	poetry export -f requirements.txt -o requirements.txt --without-hashes

run: install
	@export FLASK_APP=flask_login_without_orm/main.py &&\
	export FLASK_ENV=development &&\
	export FLASK_DEBUG=1 &&\
	flask run --host=${HOST} --port=${PORT}
