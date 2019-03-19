# IATI Website
[![Build Status](https://travis-ci.org/IATI/IATI-Standard-Website.svg?branch=master)](https://travis-ci.org/IATI/IATI-Standard-Website)

This repository hosts the new IATI website based on Django and Wagtail CMS.  A PostgreSQL database stores the underlaying content and user data.

The current scope of the project (to April 2018) focuses on the 'About IATI' and 'Publisher guidance' sections.


## Pre-requites

- Python3
- PostgreSQL


## Dev setup

Set-up and activate virtual environment
```
python3 -m venv pyenv
source pyenv/bin/activate
```

Enter into the Django project directory
```
cd iati
```

Install requirements
```
pip install -r requirements_dev.txt
```

Create a local PostgreSQL database (with appropriate user permissions. Copy the example local settings file and enter database settings accordingly.

**Note local.py should not be under version control as it contains sensitive information**

Without these steps, Django will attempt to create a SQLite3 database which will not work correctly.
```
createdb iati-website
cp iati/settings/local.py.example iati/settings/local.py
```

Make and perform Django migrations AND bespoke translations for translated fields.

**Note this will ask you to approve bespoke SQL commands**

You can auto-approve the bespoke commands by adding the flag `--noinput`
```
python manage.py makemigrations
python manage.py migrate
```

Create default pages for each of the main sections (e.g. home, about, events etc) of the website
```
python manage.py createdefaultpages
```

Create an initial superuser.

**Be sure to update your local.py file with the credentials you specify with this command**
```
python manage.py createsuperuser
```

Run a development server
```
python manage.py runserver
```

## Tests & linters

Tests are run using [pytest](https://pytest.org/) as it [provides a number of benefits](https://pytest-django.readthedocs.io/en/latest/#why-would-i-use-this-instead-of-django-s-manage-py-test-command) over stock Django test approaches.

Please be aware that very rarely tests using the database may return an OperationalError warning that the database cannot be destroyed as it is being accessed by other users. If the tests are otherwise passing it is advised that tests should be run again as this is a rare race condition glitch in pytest-django test teardown. The likelihood of this error occurring increases if subsets of tests that use the test database are run on their own. For example, if `pytest -k test_can_create_about_child_pages` is run.

```
# Run tests from the project root
pytest
```

Code linting is performed using [pylint](https://github.com/PyCQA/pylint) (with the [pylint-django](https://github.com/PyCQA/pylint-django) plugin), [flake8](http://flake8.pycqa.org) and [pydocstyle](http://www.pydocstyle.org).
```
pylint iati/
flake8 iati/
pydocstyle iati/
```

Alternatively, the Makefile can be used:
```
make -C iati test
make -C iati lint

# OR

make -C iati all
```
