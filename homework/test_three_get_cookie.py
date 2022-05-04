import requests


#python -m pytest -s .\test_three_get_cookie.py
def test_homework_cookie():
    response = requests.get('https://playground.learnqa.ru/api/homework_cookie')

    assert response.cookies, 'Cookies are missing in the response or response failed'
    print(f'Cookies: {response.cookies.items()}')

    assert 'HomeWork' in response.cookies, 'Cookie "HomeWork" does not exist'
    assert response.cookies['HomeWork'] == 'hw_value', f'Cookie value {response.cookies["HomeWork"]} does not match "hw_value"'
