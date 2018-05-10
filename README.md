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

# Make and perform Django migrations AND bespoke translations for translated fields
# Note this will ask you to approve bespoke SQL commands
python manage.py makemigrations_translation
python manage.py migrate_translation

# Create default pages for each of the main sections (e.g. home, about, events etc) of the website
python manage.py createdefaultpages

# Create an initial superuser
python manage.py createsuperuser
# Be sure to update your local.py file with the credentials you specify with this command

# Run a development server
python manage.py runserver
```

## Tests

Tests are run using [pytest](https://pytest.org/) as it [provides a number of benefits](https://pytest-django.readthedocs.io/en/latest/#why-would-i-use-this-instead-of-django-s-manage-py-test-command) over stock Django test approaches.

Please be aware that very rarely tests using the database may return an OperationalError warning that the database cannot be destroyed as it is being accessed by other users. If the tests are otherwise passing it is advised that tests should be run again as this is a rare race condition glitch in pytest-django test teardown.
```
# Run tests from the project root
pytest
```
