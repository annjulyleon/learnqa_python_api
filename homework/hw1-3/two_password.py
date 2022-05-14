import requests

BASE_URL = "https://playground.learnqa.ru/ajax/api"

with open('two_password.txt') as f:
    lines = f.read()
PASSWORDS = set(lines.split(','))


def get_auth(login: str, password: str) -> str:
    payload = {"login": login, "password": password}
    response = requests.post(f"{BASE_URL}/get_secret_password_homework",data = payload)

    return response.cookies.get("auth_cookie")


def check_auth(cookie):
    cookies = {'auth_cookie': cookie}
    response = requests.post(f"{BASE_URL}/check_auth_cookie", cookies=cookies)

    return response.text


def find_password():
    for password in PASSWORDS:
        cookie = get_auth("super_admin", password)
        check = check_auth(cookie)
        if check == 'You are authorized':
            return password
            break


print(find_password())

#print(check_auth(get_auth("super_admin","welcome")))
