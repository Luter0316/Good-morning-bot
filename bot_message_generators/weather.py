import json
import requests
import os.path

from datetime import datetime

from config.weather_config import WEATHER_CONFIG
from bot_message_generators.decorators import mute_exceptions

source_weather = None


# Проверка актуальности уже запрошенных данных
@mute_exceptions
def check_weather():
    global source_weather
    
    if os.path.exists("yandex_weather.json"):
        with open("yandex_weather.json", "r", encoding="utf-8") as weather_file:
            source_weather = json.load(weather_file)
        if datetime.strptime(source_weather["now_dt"][:10], "%Y-%m-%d").date() == datetime.now().date():
            return get_weather()
        else:
            update_weather()
            return get_weather()
    else:
        update_weather()
        return get_weather()


# Запрос данных погоды по Yandex API
def update_weather():
    global source_weather
        
    headers = {"X-Yandex-API-Key": WEATHER_CONFIG["WEATHER_API"]}
    params = {
        "lat": WEATHER_CONFIG["lat"],
        "lon": WEATHER_CONFIG["lon"],
        "lang": "ru_RU",
        #"limit": 7, # срок прогноза в днях
        #"hours": True, # наличие почасового прогноза
        #"extra": False # подробный прогноз осадков
    }
    response = requests.get(url="https://api.weather.yandex.ru/v2/forecast", params=params, headers=headers)

    if response.status_code == 200:
        source_weather = response.json()
        save_to_file(source_weather)
    else:
        return ["Данные о погоде временно недоступны!"]
    

# Возврат необходимых данных о погодных условиях
def get_weather():
    global source_weather

    return [
        f"Сейчас в городе {source_weather['geo_object']['locality']['name']}",
        f"Температура воздуха составляет {source_weather['fact']['temp']} °C ",
        f"(ощущается как: {source_weather['fact']['feels_like']} °C). ",
        f"Скорость ветра: {source_weather['fact']['wind_speed']} м/с.",
    ]
    

# Сохранение в файл
def save_to_file(data: dict) -> None:
    with open("yandex_weather.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
