import requests
import json
from json.decoder import JSONDecodeError

BASE_URL = "https://playground.learnqa.ru/api"
STRING = '{"answer":"Hello, User"}'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
    'some_header': '123'
}

"""
LESSON 2
"""


def get_hello(name: str) -> str:
    payload = {"name": name}
    response = requests.get(f"{BASE_URL}/hello", params=payload)
    return response.text


# print(get_hello("User"))

"""
JSON
"""


def format_as_json(string: str, key: str) -> str:
    obj = json.loads(string)
    if key in obj:
        return obj[key]

    return f"{key} not found"


# print(format_as_json(STRING, "answer"))


def get_and_parse(name: str, endpoint: str) -> str:
    payload = {"name": name}
    response = requests.get(f"{BASE_URL}/{endpoint}", params=payload)
    parsed_response = response.json()

    if "answer" in parsed_response:
        return parsed_response["answer"]

    return f"answer key not found"


# print(get_and_parse("user","hello"))

"""
Try and Except
"""


def get_text_as_json(endpoint: str):
    response = requests.get(f"{BASE_URL}/{endpoint}")
    try:
        parsed_response = response.json()
        return parsed_response

    except JSONDecodeError:
        print(f"Response can not be parsed as json")
        return response.text


# print(get_text_as_json("get_text"))


# Check type of called HTTP method
def check_type(method: str, endpoint: str):
    call_method = getattr(requests, method)
    if method == 'get':
        response = call_method(f"{BASE_URL}/{endpoint}", params={"param1": "value1"})
        return response.text
    elif method == 'post':
        response = call_method(f"{BASE_URL}/{endpoint}", data={"param1": "value1"})
        return response.text
    elif method == 'delete':
        response = call_method(f"{BASE_URL}/{endpoint}", data={"param1": "value1"})
        return response.text


# print(check_type("delete","check_type"))

def get_status_code(endpoint: str):
    response = requests.post(f"{BASE_URL}/{endpoint}")

    return response.status_code


# print(get_status_code("check_type"))
# print(get_status_code("get_500"))

"""
Redirects
Change from the video: add headers (returns 403 without them, change to get (in video its post)
"""


def get_redirects(endpoint: str, redirects=True):
    response = requests.get(f"{BASE_URL}/{endpoint}", headers=HEADERS, allow_redirects=redirects)

    return f'Response url: {response.url}. Status code: {response.status_code}. Redirects history: {[x.url for x in response.history]}'


# print(get_redirects("get_301",redirects=False)) # You will be redirected 301
# print(get_redirects("get_301",redirects=True)) #this actualy returns 403 without headers
# print(get_redirects("long_redirect",redirects=True))

"""
Headers
"""


def get_headers(endpoint: str):
    response = requests.get(f"{BASE_URL}/{endpoint}", headers=HEADERS)

    return f'Headers: {response.headers}. Response url: {response.url}. Status code: {response.status_code}. Response text: {response.text}'


# print(get_headers('show_all_headers'))

"""
Cookies
"""


def get_cookie(endpoint="get_auth_cookie", login="secret_login", password="secret_pass"):
    payload = {"login": login, "password": password}
    response = requests.post(f"{BASE_URL}/{endpoint}", data=payload)

    # print(f'Response url: {response.url}. Status code: {response.status_code}. Response text: {response.text}. Response cookies: {response.cookies.get("auth_cookie")} or with dict: {dict(response.cookies)}. Response headers: {response.headers}')
    return response.cookies.get("auth_cookie")


# print(get_cookie())

def check_cookie(auth_cookie=get_cookie(), endpoint='check_auth_cookie'):
    if get_cookie():
        cookies = {'auth_cookie': auth_cookie}
        response = requests.post(f"{BASE_URL}/{endpoint}", cookies=cookies)
        return response.text
    else:
        return f'Cookie not found, wrong data'


print(check_cookie())
