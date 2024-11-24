import html
import random
import re
from decimal import Decimal

import requests
from django.conf import settings

from location.models import City, Location, WeatherReport


def get_useragent():
    return random.choice(_useragent_list)


_useragent_list = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0",
]


def parse_location_html(html_text: str) -> list[tuple[str, str]]:
    pattern = r"(Praia\sd\w{1,2}\s[\w\s]+)\s-\s.*?\((.*?)\)"
    matches = re.findall(pattern, html_text, re.IGNORECASE)
    match_list = []
    for match in matches:
        beach_name = match[0].strip()
        status = match[1].strip()
        match_list.append((html.unescape(beach_name), html.unescape(status)))
    return match_list


def get_locations_html_response() -> str:
    url = "https://www.guarapari.es.gov.br/pagina/popup/2086"
    response = requests.get(
        url,
        headers={"User-Agent": get_useragent()},
    )
    response.raise_for_status()
    return response.text


def map_weather_condition(condition_id: int) -> str:
    str_config_id = str(condition_id)
    condition_digit = int(str_config_id[0])
    clearsky_digit = int(str_config_id[-1])
    match condition_digit:
        case 2:
            return "rainy"
        case 3:
            return "rainy"
        case 5:
            return "rainy"
        case 6:
            return "snowy"
        case 7:
            return "foggy"
        case 8:
            match clearsky_digit:
                case 0:
                    return "sunny"
                case _:
                    return "cloudy"
        case _:
            return "sunny"


def get_weather_report(city: City) -> tuple[Decimal, str]:
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={city.latitude}&lon={city.longitude}&units=metric&appid={settings.WEATHER_REPORT_API_KEY}"
    response = requests.get(url)
    response.raise_for_status()
    temperature = Decimal(response.json()["main"]["temp"])
    raw_condition = response.json()["weather"][0]["id"]
    condition = map_weather_condition(raw_condition)
    return temperature, condition


def upsert_weather_report(city: City):
    temperature, condition = get_weather_report(city)
    try:
        report = WeatherReport.objects.get(city=city)
        report.temperature = temperature
        report.condition = condition
        report.save()
    except WeatherReport.DoesNotExist:
        WeatherReport.objects.create(
            temperature=temperature, cmainondition=condition, city=city
        )


def infer_location_condition(condition: str) -> bool:
    good_conditions = {"PROPRIA", "PRÓPRIA", "PRÓPRIO", "PROPRIO"}
    return condition in good_conditions


def update_location_condition(location_name: str, condition: str):
    is_good = infer_location_condition(condition)
    try:
        location = Location.objects.get(name=location_name)
        location.is_good = is_good
        location.save()
    except Location.DoesNotExist:
        return


def get_and_update_location_conditions():
    location_html = get_locations_html_response()
    parsed_locations = parse_location_html(location_html)
    for location_name, condition in parsed_locations:
        update_location_condition(location_name, condition)


def update_weather_reports():
    for city in City.objects.all():
        upsert_weather_report(city)
