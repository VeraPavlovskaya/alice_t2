from flask import Flask, request, jsonify
import logging
import os
from geo import get_geo_info

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, filename='app.log',
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')


@app.route('/post', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    logging.info('Request: %r', response)
    return jsonify(response)


def handle_dialog(res, req):
    user_id = req['session']['user_id']
    if req['session']['new']:
        res['response']['text'] = \
            'Здравствуйте! Я могу сказать страну и координаты города!'
        return
    cities = get_cities(req)
    if not cities:
        res['response']['text'] = 'Вы не написали название города!'
    elif len(cities) == 1:
        res['response']['text'] = get_geo_info(cities[0])
    else:
        res['response']['text'] = 'Слишком большое количество городов!'


def get_cities(req):
    cities = []
    for entity in req['request']['nlu']['entities']:
        if entity['type'] == 'YANDEX.GEO':
            if 'city' in entity['value']:
                cities.append(entity['value']['city'])
    return cities


if __name__ == 'main':
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
