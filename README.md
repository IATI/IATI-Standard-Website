# IATI Website
[![Build Status](https://travis-ci.org/IATI/IATI-Standard-Website.svg?branch=master)](https://travis-ci.org/IATI/IATI-Standard-Website)

This repository hosts the new IATI website based on Django and Wagtail CMS.  A PostgreSQL database stores the underlaying content and user data.

The current scope of the project (to April 2018) focuses on the 'About IATI' and 'Publisher guidance' sections.


## Local Development

### Pre-requites

- Docker _(See Docker documentation for installation instructions per OS [https://docs.docker.com/install/](https://docs.docker.com/install/))_
- Docker Compose

**Important:** Ensure that native Postgres and Elasticsearch services are stopped. Docker will attempt to use these ports for its own services.

### Dev setup

Enter into the Django project directory
```
cd iati
```

Copy the example local settings file and enter database settings accordingly.

**Note local.py should not be under version control as it contains sensitive information**

```
cp iati/settings/local.py.example iati/settings/local.py
```

Build the project. The following will build linked `web`, `postgres` and `elasticsearch` containers.

```
docker-compose build
```

Start the containers in detached mode. This keeps the containers running.

```
docker-compose up -d
```

You can interact with the `web` container directly (in this example, when running a `manage.py` command), like so:

```
docker-compose run web python manage.py [command]
```

This can feel verbose, so making an alias could be a good idea.

```
echo 'alias dcrun="docker-compose run web"' >>~/.bash_profile
dcrun python manage.py [command]

echo 'alias dcmanage="docker-compose run web python manage.py"' >>~/.bash_profile
dcmanage [command]
```

Make and perform Django database migrations AND bespoke translations for translated fields.

Django will ask you to approve bespoke SQL commands for the translated fields. You can auto-approve the bespoke commands by adding the flag `--noinput`

```
docker-compose run web python manage.py makemigrations
docker-compose run web python manage.py migrate
```

Create default pages for each of the main sections (e.g. home, about, events etc) of the website
```
docker-compose run web python manage.py createdefaultpages
```

Create an initial superuser.

**Be sure to update your local.py file with the credentials you specify with this command**

```
docker-compose run web python manage.py createsuperuser
```

The website is browseable at `http://localhost/`. Make changes locally.

For logging, use:

```
docker-compose logs -f web
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
make test
make lint

# OR

make all
```
