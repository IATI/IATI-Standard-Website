# IATI Website (pre-Alpha)
This repository hosts the new IATI website based on Django and Wagtail CMS.  A PostgreSQL database stores the underlaying content and user data.

The current scope of the project (to April 2018) focuses on the 'About IATI' and 'Publisher guidance' sections.


## Pre-requites

- Python3
- SQLite or PostgreSQL


## Dev setup
```
# Set-up and activate virtual environment
python3 -m venv pyenv
source pyenv/bin/activate

# Enter into project directory
cd iati

# Install requirements
pip install -r requirements_dev.txt

# Optional: Create a local PostgreSQL database (with appropriate user permissions)
# Then, copy the example local settings file and enter database settings accordingly
# Note local.py should not be under version control as it contains sensitive information
# Without these steps, a SQLite database will be used to store data.
createdb iati-website
cp settings/local.py.example settings/local.py

# Check database migrations work and execute
python manage.py check
python manage.py migrate

# Create an initial superuser
python manage.py createsuperuser

# Run a development server
python manage.py runserver
```

## Tests & linters

Tests are run using [pytest](https://pytest.org/) as it [provides a number of benefits](https://pytest-django.readthedocs.io/en/latest/#why-would-i-use-this-instead-of-django-s-manage-py-test-command) over stock Django test approaches.
```
# Run tests from the project root
pytest
```

Code linting is performed using [pylint](https://github.com/PyCQA/pylint) (with the [pylint-django](https://github.com/PyCQA/pylint-django) plugin) and [flake8](http://flake8.pycqa.org).
```
pylint iati/
flake8 iati/
```
