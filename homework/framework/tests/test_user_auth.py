import pytest
import allure
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


@allure.epic("Authorization cases")
class TestUserAuth(BaseCase):
    exclude_params = [
        "no_cookies",
        "no_token"
    ]

    def setup(self):

        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        with allure.step("Get authorization data"):
            response_cookie = MyRequests.post("/user/login", data=data)

        self.auth_sid = self.get_cookie(response_cookie, 'auth_sid')
        self.token = self.get_header(response_cookie, 'x-csrf-token')
        self.user_id_from_login = self.get_json_value(response_cookie, 'user_id')

    @pytest.mark.smoke
    @allure.title("User authorization")
    @allure.description("This test successfully authorize user by email and password")
    def test_auth_user(self):
        response_auth = MyRequests.get(
            '/user/auth',
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid})

        Assertions.assert_json_value_by_name(
            response_auth,
            "user_id",
            self.user_id_from_login,
            f'UserId from login ({self.user_id_from_login}) is not equal UserId from auth'
        )

    @allure.title("Authorization with {condition}")
    @allure.description("This test check authorization status without sending auth cookie or token")
    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):

        if condition == 'no_cookie':
            response_cookie_header = MyRequests.get(
                '/user/auth',
                headers={'x-csrf-token': self.token}
            )
        else:
            response_cookie_header = MyRequests.get(
                '/user/auth',
                cookies={'auth_sid': self.auth_sid}
            )

        Assertions.assert_json_value_by_name(
            response_cookie_header,
            "user_id",
            0,
            f"User is authorized with {condition}"
        )
