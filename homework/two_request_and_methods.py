import requests
from itertools import product
from typing import Optional

BASE_URL = 'https://playground.learnqa.ru/api'
ENDPOINT = 'compare_query_type'
VERBS = ['get', 'post', 'put', 'delete']


# it actually works fine when providing both data and params for any request? No need for elif logic at all
def check_query_type(request_verb: str, request_param: Optional[str] = None) -> dict:
    call_requests_verb = getattr(requests, request_verb)
    if request_param and request_verb == 'get':
        response = call_requests_verb(f"{BASE_URL}/{ENDPOINT}", params={"method": request_param.upper()})
    elif request_param and request_verb != 'get':
        response = call_requests_verb(f"{BASE_URL}/{ENDPOINT}", data={"method": request_param.upper()})
    else:
        response = call_requests_verb(f"{BASE_URL}/{ENDPOINT}")

    return {"verb": request_verb,
            "param": request_param,
            "status": response.status_code,
            "message": response.text
            }


# 1. Any request without method in params (or data)
any_request_verb = check_query_type('get')
print(
    f'1. Send request with "get", no params.\nResponse text: {any_request_verb.get("message")}.\
    \nResponse status: {any_request_verb.get("status")}')  # Wrong method provided. #200

# 2. Request which is not from the list VERBS
any_other_verb = check_query_type('head')
print(
    f'\n2. Send request with "head", no params.\nResponse text: {any_other_verb.get("message")}.\
    \nResponse status: {any_other_verb.get("status")}') \
    # None. #400

# 3. Provide method in params (or data)
post_type_verb = check_query_type('post', 'post')
print(
    f'\n3.1 Send request with "post", and param "post".\nResponse text: {post_type_verb.get("message")}.\
    \nResponse status: {post_type_verb.get("status")}')  # {"success":"!"} #200

get_type_verb = check_query_type('get', 'get')
print(
    f'\n3.2 Send request with "get", and param "get".\nResponse text: {get_type_verb.get("message")}.\
    \nResponse status: {get_type_verb.get("status")}')  # {"success":"!"} #200

# 4. Check all possible combinations
errors = []

for verb, param in product(VERBS, repeat=2):
    report = check_query_type(verb, param.upper())
    print(report)
    if verb == param and report.get('message') != '{"success":"!"}':
        errors.append(report)
    elif verb != param and report.get('message') != 'Wrong method provided':
        errors.append(report)

print(f'\nErrors: {errors}')
