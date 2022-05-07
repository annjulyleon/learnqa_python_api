import pytest
import requests
from libs.base_case import BaseCase
from libs.assertions import Assertions


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

        self.auth_sid = self.get_cookie(response_cookie, 'auth_sid')
        self.token = self.get_header(response_cookie, 'x-csrf-token')
        self.user_id_from_login = self.get_json_value(response_cookie, 'user_id')

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