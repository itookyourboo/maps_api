import requests
import os
import sys


def give_me_an_image(coords, zoom, layer_type):
    response = None
    try:
        payload = {
            'apikey': 'd1439a14-b3fc-44e5-a9f7-c121f92cbe63',
            'll': coords,
            'z': zoom,
            'l': layer_type
        }
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

    form = 'png' if layer_type != 'sat' else 'jpg'
    map_file = "map." + form
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)

    return map_file