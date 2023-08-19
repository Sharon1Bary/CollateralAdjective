import webbrowser

from fastapi import APIRouter, FastAPI
from fastapi.exceptions import ResponseValidationError

from src.lib.logic.scraping.scraping import scraping_provided_url, create_html_page
from src.lib.models.CollateralAdjective import CollateralAdjective

app = FastAPI(title="Animal Collateral Adjectives")
router_scraping_url = APIRouter()
router_scraping_url_to_html = APIRouter()


# The app Health Check.
@app.get('/', status_code=200, tags=['Health Check'])
def health_check():
    return "Animal Collateral Adjectives app is up and running."


@router_scraping_url.get("/collateral_adjective/", status_code=200, response_model=CollateralAdjective)
async def scraping_url(url: str):
    """
        Based on the following URL - https://en.wikipedia.org/wiki/List_of_animal_names, the api returns a json included
        all the animals by Collateral Adjectives and their future pic location. \n
        :param url: str \n
        :return: CollateralAdjective. \n
    """
    try:
        # Start the scraping.
        return scraping_provided_url(url=url, is_bonus=False)
    except ValueError:
        logger.error('Error occurred: That was not a valid URL')
    except KeyError as el:
        logger.error(f'Error occurred: {el}')
    except ResponseValidationError as el:
        logger.error(f'Error occurred: {el}')
    except Exception as el:
        logger.error(f'Error occurred: {el}')


@router_scraping_url_to_html.get("/html/", status_code=200)
async def make_html(url: str):
    """
        Bonus: based on the following URL - https://en.wikipedia.org/wiki/List_of_animal_names, the api returns a HTML
         File included a table with all the animals Collateral Adjectives. \n
         To see the animal pic, please click the name (link), the animal pics locate at /tmp. \n
        :param url: str \n
        :return: HTML file.
    """
    try:
        # For the bonus question - create an html page include a table with all the collateral adjective and their animals list.
        # Each animal in the table link to animal picture that stored at /tmp/AnimalName.jpg.
        return create_html_page(c_as=scraping_provided_url(url=url, is_bonus=True))
    except ValueError:
        logger.error('Error occurred: That was not a valid URL')
    except KeyError as el:
        logger.error(f'Error occurred: {el}')
    except OSError as el:
        logger.error(f'Error occurred: {el}')
    except ResponseValidationError as el:
        logger.error(f'Error occurred: {el}')
    except Exception as el:
        logger.error(f'Error occurred: {el}')


# Add the endpoints to the FastAPI
app.include_router(router_scraping_url, tags=["Create Animal Collateral Adjectives JSON"])
app.include_router(router_scraping_url_to_html, tags=["Create Animal Collateral Adjectives HTML.file"])

# Once the app is running, it open the FastAPI swagger as well.
webbrowser.open('http://127.0.0.1:8000/docs#')


if __name__ == "__main__":
    """
        The main is launching the app and creating a logger to be able store the error logs in future.
        To login the app / swagger please go to - http://127.0.0.1:8000/docs#/
    """
    import uvicorn
    import logging
    import sys

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    try:
        uvicorn.run(app, port=8000, log_level="debug")
    except Exception as e:
        logger.exception(e)
