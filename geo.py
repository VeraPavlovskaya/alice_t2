import requests

apikey = "40d1649f-0493-4b70-98ba-98533de7710b"


def get_geo_info(city_name):
    try:
        url = "https://geocode-maps.yandex.ru/1.x/"
        params = {
            'apikey': apikey,
            'geocode': city_name,
            'format': 'json'

        }
        data = requests.get(url, params).json()
        coords_string = data['response']['GeoObjectCollection'][
            'featureMember'][0]['GeoObject']['Point']['pos']
        coords, crd = map(float, coords_string.split())
        country_name = data['response']['GeoObjectCollection']['featureMember'][0][
            'GeoObject']['metaDataProperty']['GeocoderMetaData'][
            'AddressDetails']['Country']['CountryName']
        return f"Страна - {country_name}, координаты - {coords}, {crd}"
    except Exception as excep:
        return excep
