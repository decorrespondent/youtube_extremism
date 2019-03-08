.PHONY: help guard-virtual-env basedependencies env clean

guard-virtual-env: ## Exits if python virtual environment is not set
	@ if [ "${VIRTUAL_ENV}" = "" ]; then \
		echo "Virtual environment is not active. Activate with 'source venv/bin/activate'"; \
		exit 1; \
	fi

clean: ## Removes all build artifacts
	for build_dir_glob in \
		build \
		dist \
		.eggs \
		*.egg-info \
		*.pyc \
		*.pyo \
		*~ \
		__pycache__ \
		.pytest_cache \
		.coverage \
		htmlcov; \
	do find . -name "$$build_dir_glob" -exec rm -fr {} +; done

basedependencies: guard-virtual-env clean
	pip3 install --upgrade pip setuptools wheel

env:
	pip3 install --upgrade virtualenv
	virtualenv venv

dependencies: basedependencies
	pip3 install -r requirements.txt

development: dependencies
	pip3 install -e .[dev]

test: clean development
	python3 setup.py test

coverage: clean development
	coverage run -m pytest
	coverage report
	coverage html
	open htmlcov/index.html

install: dependencies
	python3 setup.py install
