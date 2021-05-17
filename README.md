# IATI Website

![](https://github.com/IATI/IATI-Standard-Website/workflows/CI/badge.svg)

This repository hosts the new IATI website based on Django and Wagtail CMS. A PostgreSQL database stores the underlaying content and user data.

## Local Development

### Pre-requites

- Docker _(See Docker documentation for installation instructions per OS [https://docs.docker.com/install/](https://docs.docker.com/install/))_
- Docker Compose

**Important:** Ensure that native Postgres service is stopped. Docker will attempt to use these ports for its own service.

### Dev setup

#### Docker-compose set up

- Set a SECRET_KEY

Build the project. The following will build linked `web` and `postgres` containers.

```
docker-compose -f docker-compose.dev.yml build
```

Start the containers in detached mode. This will run migrations and run the Django server. Using in detached (`-d`) mode means that the containers will continue to run in the background - ommitting the `-d` flag will mean that the containers will run only until the command is exited.

```
docker-compose -f docker-compose.dev.yml up -d
```

See the status of your containers by using

```
docker ps
```

#### Docker-compose commands

You can interact with the `web` container directly (in this example, when running a `manage.py` command), like so:

```
docker-compose -f docker-compose.dev.yml exec web python manage.py [command]
```

This can feel verbose, so making an alias could be a good idea.

```
echo 'alias dcrun="docker-compose -f docker-compose.dev.yml exec web"' >>~/.bash_profile
dcrun python manage.py [command]

echo 'alias dcmanage="docker-compose -f docker-compose.dev.yml exec web python manage.py"' >>~/.bash_profile
dcmanage [command]
```

Other useful commands (use with caution)

```
docker kill $(docker ps -q)  //stop all containers

docker rm $(docker ps -a -q)  //remove all containers

docker rmi $(docker images -q) //remove all images

docker volume ls -qf dangling=true | xargs -r docker volume rm  //remove all volumes

```

Create default pages for each of the main sections (e.g. home, about, events etc) of the website

```
docker-compose -f docker-compose.dev.yml exec web python manage.py createdefaultpages
```

Create an initial superuser.

```
docker-compose -f docker-compose.dev.yml exec web python manage.py createsuperuser
```

The website is browseable at `http://localhost/`. Make changes locally.

For logging, use:

```
docker-compose -f docker-compose.dev.yml logs -f web
```

#### Debugging

- Set a breakpoint in code `import pdb; pdb.set_trace()`
- SSH into running Docker container `docker exec -it <container id> /bin/sh`
- Run command `python manage.py <command>`
- debugging away in your terminal session

## Tests & linters

Tests are run using [pytest](https://pytest.org/) as it [provides a number of benefits](https://pytest-django.readthedocs.io/en/latest/#why-would-i-use-this-instead-of-django-s-manage-py-test-command) over stock Django test approaches.

Please be aware that very rarely tests using the database may return an OperationalError warning that the database cannot be destroyed as it is being accessed by other users. If the tests are otherwise passing it is advised that tests should be run again as this is a rare race condition glitch in pytest-django test teardown. The likelihood of this error occurring increases if subsets of tests that use the test database are run on their own. For example, if `pytest -k test_can_create_about_child_pages` is run.

Configurations for tests and linting can be found in the `iati/` directory.

```
# Run tests from the project root
docker-compose -f docker-compose.dev.yml exec web pytest
```

Code linting is performed using [pylint](https://github.com/PyCQA/pylint) (with the [pylint-django](https://github.com/PyCQA/pylint-django) plugin), [flake8](http://flake8.pycqa.org) and [pydocstyle](http://www.pydocstyle.org).

```
docker-compose -f docker-compose.dev.yml exec web pylint .
docker-compose -f docker-compose.dev.yml exec web flake8
docker-compose -f docker-compose.dev.yml exec web pydocstyle
```

Alternatively, the Makefile can be used:

```
docker-compose -f docker-compose.dev.yml exec web make test
docker-compose -f docker-compose.dev.yml exec web make lint

# OR

docker-compose -f docker-compose.dev.yml exec web make all
```

## Moving from `pyenv` development environment to `docker` development environment

Previous iterations of this project utilised `pyenv` for development. This included using postgres natively, and adding local database credentials to `local.py`.

- Firstly, remove the `pyenv` directory.

```
rm -r pyenv/
```

- Secondly, remove the `DATABASES` dict from `local.py` entirely. The database config is now handled in `dev.py`, and does not need user customisation.

If you are receiving the following error on `web`:

```
psql: could not connect to server: Connection refused Is the server running on host "" and accepting TCP/IP connections on port 5432?
```

First try replacing `POSTGRES_PASSWORD=''` with `POSTGRES_HOST_AUTH_METHOD=trust` in `docker-compose.dev.yml`

Follow the instructions on [this SO answer](https://stackoverflow.com/a/41161674). Your postgres configuration may need amending to listen for all addresses. Postgres will need restarting, and importantly, **your computer will require a restart** for changes to take place.
