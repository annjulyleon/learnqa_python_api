import pytest
import requests
from libs.base_case import BaseCase
from libs.assertions import Assertions
"""
LESSON 3
"""


@pytest.mark.skip(reason="These are tests from the first video")
class TestExample:
    # python -m pytest test_examples.py -k "test_check_math"
    def test_check_math(self):
        a = 5
        b = 9
        expected = 14
        assert a + b == expected, f'{expected} is not equal to {a + b}'

    def test_check_math_wrong(self):
        a = 5
        b = 11
        expected = 14
        assert a + b == 14, f'{expected} is not equal to {a + b}'


# python -m pytest test_examples.py
@pytest.mark.skip(reason="These are tests from the third and second videos")
class TestFirstApi:
    """
    Test endpoint 'hello'
    """
    names = [
        ("Anna"),
        ("Grisha"),
        ("")
    ]

    # set name of variable in quotes, and list of values. Test will be executed with each value
    # i actually don't like multiple asserts and conditional logic in single test o_O
    @pytest.mark.parametrize('name', names)
    def test_hello_call(self, name):
        url = 'https://playground.learnqa.ru/api/hello'
        data = {'name': name}

        response = requests.get(url, params=data)

        assert response.status_code == 200, f'Expected "200", got "{response.status_code}"'

        response_dict = response.json()

        assert "answer" in response_dict, '"answer" field is not present in the response'

        if len(name) == 0:
            expected_response_text = f'Hello, someone'
        else:
            expected_response_text = f'Hello, {name}'

        actual_response_text = response_dict["answer"]

        assert actual_response_text == expected_response_text, f"Actual text is not correct, expected '{expected_response_text}', got '{actual_response_text}'"


"""
Positive and negative tests, setup
"""

@pytest.mark.skip(reason="These are tests without basecase class")
class TestUserAuth:
    exclude_params = [
        "no_cookies",
        "no_token"
    ]

    def setup(self):
        self.base_url = 'https://playground.learnqa.ru/api/user'
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response_cookie = requests.post(f'{self.base_url}/login', data=data)
        assert "auth_sid" in response_cookie.cookies, "Auth cookie is missing in the response"
        assert "x-csrf-token" in response_cookie.headers, 'CSRF token is missing in the response'
        assert "user_id" in response_cookie.json(), 'User id is missing in the response'

        self.auth_sid = response_cookie.cookies.get('auth_sid')
        self.token = response_cookie.headers.get('x-csrf-token')
        self.user_id_from_login = response_cookie.json()["user_id"]

    def test_auth_user(self):
        response_auth = requests.get(
            f'{self.base_url}/auth',
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid})
        assert "user_id" in response_auth.json(), "User_id is missing from the second response"

        user_id_from_auth = response_auth.json()["user_id"]

        assert self.user_id_from_login == user_id_from_auth, f'UserId from login ({self.user_id_from_login}) is not equal UserId from auth ({user_id_from_auth})'

    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):

        if condition == 'no_cookie':
            response_cookie_header = requests.get(
                f'{self.base_url}/auth',
                headers={'x-csrf-token': self.token}
            )
        else:
            response_cookie_header = requests.get(
                f'{self.base_url}/auth',
                cookies={'auth_sid': self.auth_sid}
            )

        assert "user_id" in response_cookie_header.json(), "UserId is missing from the response"

        user_id_from_auth = response_cookie_header.json()["user_id"]

        # user must not be authorized
        assert user_id_from_auth == 0, f"User is authorized with {condition}"

"""
This are test with BaseClass adn Assertions, hurray!
"""


class TestUserAuth(BaseCase):
    exclude_params = [
        "no_cookies",
        "no_token"
    ]

    def setup(self):
        self.base_url = 'https://playground.learnqa.ru/api/user'
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response_cookie = requests.post(f'{self.base_url}/login', data=data)
        self.auth_sid = self.get_cookie(response_cookie,'auth_sid')
        self.token = self.get_header(response_cookie,'x-csrf-token')
        self.user_id_from_login = self.get_json_value(response_cookie,'user_id')

    def test_auth_user(self):
        response_auth = requests.get(
            f'{self.base_url}/auth',
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid})

        Assertions.assert_json_value_by_name(
            response_auth,
            "user_id",
            self.user_id_from_login,
            f'UserId from login ({self.user_id_from_login}) is not equal UserId from auth'
        )

    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):

        if condition == 'no_cookie':
            response_cookie_header = requests.get(
                f'{self.base_url}/auth',
                headers={'x-csrf-token': self.token}
            )
        else:
            response_cookie_header = requests.get(
                f'{self.base_url}/auth',
                cookies={'auth_sid': self.auth_sid}
            )

        Assertions.assert_json_value_by_name(
            response_cookie_header,
            "user_id",
            0,
            f"User is authorized with {condition}"
        )