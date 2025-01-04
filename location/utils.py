import html
import json
import random
import re
from base64 import b64decode
from datetime import date
from decimal import Decimal

import requests
from bs4 import BeautifulSoup
from django.conf import settings
from google.auth.transport.requests import Request
from google.oauth2 import service_account

from location.models import City, CityURL, Location, WeatherReport


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


def transform_date(date_str: str) -> date:
    month_map = {
        "janeiro": 1,
        "fevereiro": 2,
        "março": 3,
        "abril": 4,
        "maio": 5,
        "junho": 6,
        "julho": 7,
        "agosto": 8,
        "setembro": 9,
        "outubro": 10,
        "novembro": 11,
        "dezembro": 12,
    }

    date_part = date_str.split(", ")[1]

    date_obj = date(
        year=int(date_part.split()[-1]),
        month=month_map[date_part.split()[-3]],
        day=int(date_part.split()[0]),
    )
    return date_obj


def parse_date_ddmmyyyy(date_str: str) -> date:
    day, month, year = map(int, date_str.split("/"))
    return date(year, month, day)


def parse_date_html(html_text: str) -> tuple[str, bool]:
    date_pattern = r"Data de Publicação: ([^<]+)"
    match = re.search(date_pattern, html_text)
    needs_transformation = True
    if not match:
        date_pattern = "RESULTADO EM ([^<]+)"
        match = re.search(date_pattern, html_text)
        needs_transformation = False
    date_str = match.group(1)
    return date_str, needs_transformation


def parse_location_html(html_text: str) -> list[tuple[str, str]]:
    pattern = r"Praia\sd\w{1,2}\s([\w\s]+)\s-\s.* - (.+)(<br\s*\/?>)?"
    matches = re.findall(pattern, html_text, re.IGNORECASE)
    match_list = []
    for match in matches:
        beach_name = html.unescape(match[0].strip())
        status = (
            html.unescape(match[1].strip())
            .replace("<br />", "")
            .replace("<br/>", "")
            .replace("<br>", "")
        )
        match_list.append((beach_name, status))
    return match_list


def assert_is_most_recent(last_posted_at: date, html_text: str) -> tuple[bool, date]:
    parsed_date_str, needs_transformation = parse_date_html(html_text)
    if needs_transformation:
        parsed_date = transform_date(parsed_date_str)
    else:
        parsed_date = parse_date_ddmmyyyy(parsed_date_str)
    return parsed_date >= last_posted_at, parsed_date


def query_location_url(url: str) -> str:
    response = requests.get(
        url,
        headers={"User-Agent": get_useragent()},
    )
    response.raise_for_status()
    return response.text


def get_all_balneabilidade_urls(html_text: str) -> list[str]:
    default_balneabilidade_url = (
        "https://www.guarapari.es.gov.br/pagina/ler/2086/balneabilidade"
    )
    soup = BeautifulSoup(html_text, "html.parser")
    div = soup.find("div", class_="list-group list-group-legislacao")
    urls = [a["href"] for a in div.find_all("a", href=True)] + [
        default_balneabilidade_url
    ]
    return urls


def get_updated_url(city: City) -> str:
    city_url = CityURL.objects.get(city=city)
    last_posted_at = city_url.posted_at
    query_url = city_url.query_url
    raw_publications = query_location_url(query_url)
    balneabilidade_urls = get_all_balneabilidade_urls(raw_publications)
    for url in balneabilidade_urls:
        html_text = query_location_url(url)
        is_most_recent, new_last_posted_at = assert_is_most_recent(
            last_posted_at, html_text
        )
        if is_most_recent:
            city_url.url = url
            city_url.posted_at = new_last_posted_at
    city_url.save()
    return city_url.url


def get_locations_html_response() -> str:
    url = get_updated_url(City.objects.first())
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
            temperature=temperature, condition=condition, city=city
        )


def infer_location_condition(condition: str) -> bool:
    good_conditions = {"PROPRIA", "PRÓPRIA", "PRÓPRIO", "PROPRIO"}
    return condition in good_conditions


def update_location_condition(location_name: str, condition: str):
    is_good = infer_location_condition(condition)
    try:
        if location_name.startswith("Morro"):
            location_name = f"Praia do {location_name}"
            location = Location.objects.get(name=location_name)
        else:
            location = Location.objects.filter(
                name__unaccent__icontains=location_name
            ).first()
        if not location:
            return
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


def call_cloud_run_endpoint(url: str, data: dict = dict()):
    b64_cred = settings.GCP_SA_KEY
    transformed_sa = b64decode(b64_cred).decode("utf-8")
    credentials = service_account.IDTokenCredentials.from_service_account_info(
        info=json.loads(transformed_sa),
        target_audience=settings.CLOUD_RUN_ENDPOINT,
    )
    request = Request()
    credentials.refresh(request)
    headers = {
        "Authorization": f"Bearer {credentials.token}",
        "Content-Type": "application/json",
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
