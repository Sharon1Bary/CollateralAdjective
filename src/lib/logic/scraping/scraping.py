import os
import requests
import concurrent.futures

from collections import defaultdict
from bs4 import BeautifulSoup

from src.lib.models.Animal import Animal
from src.lib.models.CollateralAdjective import CollateralAdjective


def scraping_provided_url(url: str, is_bonus: bool) -> CollateralAdjective:
    """
    Get all the animals from the animal WIKI url using BeautifulSoup,
    send them to the handler and return a JSON with all the collateral_adjs.

        :param url: https://en.wikipedia.org/wiki/List_of_animal_names
        :param is_bonus: bool for the Bonus question.
        :return:
    """
    # based on url provided get the html.
    html = BeautifulSoup(requests.get(url).content, 'html.parser')
    # get the animal tags from the html if the tag is table with class wikitable sortable.
    animal_tags = html.find_all("table", {"class": "wikitable sortable"})[1].find_all("tr")[2:]

    return scraping_provided_url_handler(animal_tags=animal_tags, is_bonus=is_bonus)


def scraping_provided_url_handler(animal_tags: list, is_bonus: bool):
    """
    The handler get all the animal_tags and based on a collateral_adj in append the related animals.
    If the bonus is true, we make a Thread to download each animal pic locally based on the img HTML in animal_tags.
    The threads using a ThreadPoolExecutor to use a thread pool.
    :param animal_tags:
    :param is_bonus:
    :return:
    """
    collateral_adjs = defaultdict(list)
    # Create the threading pool for the animal imgs.
    thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=2)

    for tag in animal_tags:
        if len(tag.find_all("td")) > 5 and tag.td.a['href']:
            # for the bonus question - create thread for each animal img download.
            if is_bonus:
                thread_pool.submit(scraping_animal_picture,
                                   animal_url=tag.td.a['href'],
                                   animal_name=tag.td.a.string.split('/')[0])
            for collateral_adj in tag.find_all("td")[5].get_text(separator=' ').split(' '):
                if collateral_adj.isalpha():
                    collateral_adjs[collateral_adj].append(
                        Animal(name=tag.td.a.string, img_link=f'/tmp/{tag.td.a.string}'))
    return CollateralAdjective(collateral_adjective=collateral_adjs)


def create_html_page(c_as: CollateralAdjective):
    """
    Build the HTML file - it's a table include the following,
    collateral_adj and the animals related to the collateral_adj, also a link (href) to the animal picture.
    :param c_as:
    :return:
    """
    data = ""
    for collateral_adjective in c_as.collateral_adjective:
        data += f"<td style='color:DodgerBlue;'>{collateral_adjective} </td>"
        for animal in c_as.collateral_adjective[collateral_adjective]:
            data += f" <td style='color:SlateBlue;'> <a href={animal.img_link}.jpg> <div>{animal.name}</div></td></a>"
        data += "<tr>"
    data = f"<table border=2>{data}<table>"

    with open("file.html", "w") as file:
        file.write(data)
    os.startfile("file.html")
    return data


def scraping_animal_picture(animal_url: str, animal_name: str):
    """
    Bases on a animal url we are downloading the animal picture and storing it in /tmp/AnimalName.jpg.
    :param animal_url:
    :param animal_name:
    :return:
    """
    html = BeautifulSoup(requests.get(f'https://en.wikipedia.org/{animal_url}').content, 'html.parser')
    for img in html.find_all('img'):
        if animal_name in img['src']:
            response = \
                requests.get(f'https:{img["src"]}',
                             headers={'User-Agent': 'CoolBot/0.0 (https://example.org/coolbot/; coolbot@example.org)'})
            with open(f'/tmp/{animal_name}.jpg', 'wb') as handler:
                handler.write(response.content)
            break
