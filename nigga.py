import requests
import os
import sys
import math


def give_me_an_image(coords, zoom, layer_type, point=None):
    response = None
    try:
        payload = {
            'll': coords,
            'z': zoom,
            'l': layer_type
        }
        if point:
            payload['pt'] = point
        map = "http://static-maps.yandex.ru/1.x"
        response = requests.get(map, params=payload)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
    except:
        print("Запрос не удалось выполнить. Проверьте наличие сети Интернет.")
        sys.exit(1)

    return response.content


def find_object(object):
    url = "http://geocode-maps.yandex.ru/1.x"
    payload = {
        "geocode": object,
        "format": "json",
    }
    response = requests.get(url, params=payload).json()
    toponym = response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
    try:
        index = toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"]
    except:
        index = ""
    toponym_coodrinates = toponym["Point"]["pos"].replace(" ", ",")
    return toponym_coodrinates, toponym_address, index


def find_orginization(coords):
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

    search_params = {
        "apikey": api_key,
        "lang": "ru_RU",
        "ll": coords,
        'spn': ','.join(map(str, calculate_spn(list(map(float, coords.split(',')))))),
        'rspn': '1',
        "type": "biz",
        'results': '50'
    }
    try:
        response = requests.get(search_api_server, params=search_params)
        if not response:
            return '', 'Организаций не найдено'

        json_response = response.json()

        for org in json_response["features"]:
            org_coords = org['geometry']['coordinates']
            if lonlat_distance(list(map(float, coords.split(','))), org_coords) <= 50:
                org_name = org["properties"]["CompanyMetaData"]["name"]
                return ','.join(map(str, org_coords)), org_name
        return '', 'Организаций не найдено'
    except:
        return '', 'Ошибка запроса'


def lonlat_distance(a, b):
    degree_to_meters_factor = 111 * 1000  # 111 километров в метрах
    a_lon, a_lat = a
    b_lon, b_lat = b

    # Берем среднюю по широте точку и считаем коэффициент для нее.
    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)

    # Вычисляем смещения в метрах по вертикали и горизонтали.
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor

    # Вычисляем расстояние между точками.
    distance = math.sqrt(dx * dx + dy * dy)

    return distance

def calculate_spn(coords):
    meters_to_degree_factor = 50 * 2 / (111 * 1000)
    return meters_to_degree_factor / math.cos(math.radians(coords[1])), meters_to_degree_factor