import datetime
import xml.etree.ElementTree as Et
from logging import getLogger

import requests

from bot_message_generators.decorators import mute_exceptions

logger = getLogger("console")

SITE_URL = 'https://cbr.ru/'

@mute_exceptions
def get_exchange_rates():
    currency_codes = [
        "R01239", # Евро
        "R01235", # Доллар
    ]

    row = "{name}/{short} - {value} руб."
    rows = [f"*Курсы валют, источник - Центробанк РФ ({SITE_URL}).*", ]

    date_str = datetime.datetime.now().strftime("%d/%m/%Y")
    res = requests.get(
        f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={date_str}"
    )
    if res.ok:
        root = Et.fromstring(res.content)
        for i in root:
            if i.attrib.get("ID") in currency_codes:
                rows.append(row.format(
                    name=next(i.iter("Name")).text,
                    short=next(i.iter("CharCode")).text,
                    value=next(i.iter("Value")).text,
                ))
    else:
        logger.warning(f"Status code is {res.status_code}")
    return rows
