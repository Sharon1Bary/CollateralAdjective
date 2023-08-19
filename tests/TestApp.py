import requests
import pytest

from bs4 import BeautifulSoup

from src.lib.logic.scraping.scraping import scraping_provided_url_handler
from src.lib.models.CollateralAdjective import CollateralAdjective


# data for the tests
@pytest.fixture
def url_res_data():
    params = {
        'url': 'https://en.wikipedia.org/wiki/List_of_animal_names',
    }
    response = requests.get('http://127.0.0.1:8000/collateral_adjective/',
                            params=params,
                            headers={'accept': 'application/json'})
    return response


# data for the tests
@pytest.fixture
def animal_tags_data():
    url = 'https://en.wikipedia.org/wiki/List_of_animal_names'

    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    animal_tags = soup.find_all("table", {"class": "wikitable sortable"})[1].find_all("tr")[2:]
    return animal_tags


def test_check_connection(url_res_data):
    """
        Check the connection to wiki using the API (Please make sure the app is running).
    """
    print(url_res_data)
    assert url_res_data.status_code == 200


def test_scraping_provided_url_handler(animal_tags_data):
    collateral_adjectives = scraping_provided_url_handler(animal_tags=animal_tags_data,
                                                          is_bonus=False)
    assert isinstance(collateral_adjectives, CollateralAdjective)
    assert len(collateral_adjectives.collateral_adjective) >= 193
