import requests


#python -m pytest -s .\test_three_get_header.py
def test_homework_header():
    response = requests.get('https://playground.learnqa.ru/api/homework_header')

    print(f'Headers: {response.headers.items()}')

    assert 'x-secret-homework-header' in response.headers, 'Header "x-secret-homework-header" does not exist'
    assert response.headers['x-secret-homework-header'] == 'Some secret value', f'Header value {response.headers["x-secret-homework-header"]} does not match "Some secret value"'
