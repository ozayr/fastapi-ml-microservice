PY_ENV =new-env
SHELL=/bin/bash
setup:
	python3 -m venv $(PY_ENV); \
	if [ ! -f "/bin/hadolint" ]; then \
		wget -O /bin/hadolint https://github.com/hadolint/hadolint/releases/download/v1.16.3/hadolint-Linux-x86_64 &&\
		chmod +x /bin/hadolint; \
	fi;


install:
	source $(PY_ENV)/bin/activate; \
	pip install --upgrade pip && \
	pip install -r requirements.txt

test:
	pytest

lint:
	hadolint Dockerfile
	source $(PY_ENV)/bin/activate;
	pylint --ignore=tests --disable=R,C,W1203,E0611 api 

all: setup install lint test
