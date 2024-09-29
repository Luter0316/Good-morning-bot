from bot_message_generators.exchange_rates import get_exchange_rates
from bot_message_generators.greetings import get_greetings
from bot_message_generators.rbc_news import get_rbc_news
from bot_message_generators.weather import check_weather


def get_message():
    rows = []
    delimiter = "------------------------------------------------------"

    for i in [
        get_greetings,
        get_exchange_rates,
        get_rbc_news,
        check_weather,
    ]:
        rows.extend(i())
        rows.append(delimiter)

    return "\n".join(rows)
