import requests

DOMAIN = 'https://playground.learnqa.ru/api'


def get_response_text(endpoint):
    response = requests.get(f'{DOMAIN}/{endpoint}')
    print(response.text)


get_response_text('get_text')
