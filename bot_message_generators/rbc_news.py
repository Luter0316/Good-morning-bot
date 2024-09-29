import requests
from bs4 import BeautifulSoup

from bot_message_generators.decorators import mute_exceptions

SITE_URL = 'https://www.rbc.ru/'


@mute_exceptions
def get_rbc_news():
    response = requests.get(SITE_URL)
    soup = BeautifulSoup(response.text, 'html.parser')


    row = "[{title}]({url})"

    news_titles = [f"*Новости с сайта {SITE_URL}*"]

    for title in soup.find_all('span', class_='main__big__title-wrap'):
        news_titles.append(
            row.format(
                title=title.text,
                url=SITE_URL
            )
        )

    for title in soup.find_all('span', class_='main__feed__title-wrap'):
        news_titles.append(
            row.format(
                title=title.text,
                url=SITE_URL
            )
        )


    return news_titles
