import pytest
from home.factories import HomePageFactory


@pytest.mark.django_db
def test_home_page(client):
    home_page = HomePageFactory(title='Home', parent=None)
    assert home_page.title == 'Home'