# new-website
New IATI (about &amp; guidance) website based on Django and Wagtail CMS


## Dev setup
```
# Set-up and activate virtual environment
python3 -m venv pyenv
source pyenv/bin/activate

# Enter into project directory
cd iati

# Install requirements
pip install -r requirements.txt

# Create a local postgres database (with appropriate user permissions)
# settings/base.py expects username 'myusername' and password 'mypassword'
createdb iati-website

# Check database migrations work and execute
python manage.py check
python manage.py migrate

# Run a development server
python manage.py createsuperuser
```
