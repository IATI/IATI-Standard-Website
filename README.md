# IATI Website (pre-Alpha)
This repository hosts the new IATI website based on Django and Wagtail CMS.  A PostgreSQL database stores the underlaying content and user data.

The current scope of the project (to April 2018) focuses on the 'About IATI' and 'Publisher guidance' sections.


# Pre-requite packages

- Python3
- PostgreSQL


## Dev setup
```
# Set-up and activate virtual environment
python3 -m venv pyenv
source pyenv/bin/activate

# Enter into project directory
cd iati

# Install requirements
pip install -r requirements.txt

# Create a local PostgreSQL database (with appropriate user permissions)
# settings/base.py expects username 'myusername' and password 'mypassword'
# You can also use settings/local.py to set database credentials for your local instance
createdb iati-website

# Check database migrations work and execute
python manage.py check
python manage.py migrate

# Create an initial superuser
python manage.py createsuperuser

# Run a development server
python manage.py run server
```
