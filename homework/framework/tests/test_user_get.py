import allure

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


@allure.epic("Get user cases")
class TestUserGet(BaseCase):
    default_data = {
        "email": "vinkotov@example.com",
        "password": "1234"
    }

    @allure.description("This test ensure unauthorized user can see only her username")
    def test_get_user_details_not_auth(self):
        response = MyRequests.get('/user/2')

        Assertions.assert_json_has_key(response, 'username')
        Assertions.assert_json_has_not_key(response, 'email')
        Assertions.assert_json_has_not_key(response, 'firstName')
        Assertions.assert_json_has_not_key(response, 'lastName')

    @allure.description("This test ensure authorized user can see all her user info fields")
    def test_get_user_details_auth_as_same_user(self):

        response_auth = MyRequests.post("/user/login", data=self.default_data)
        auth_sid = self.get_cookie(response_auth, "auth_sid")
        token = self.get_header(response_auth, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response_auth, "user_id")

        response_with_details = MyRequests.get(f'/user/{user_id_from_auth_method}',
                                               headers={"x-csrf-token": token},
                                               cookies={"auth_sid": auth_sid})

        Assertions.assert_json_has_keys(response_with_details, ['username', 'email', 'firstName', 'lastName'])

    # python -m pytest -s .\tests\test_user_get.py -k test_get_user_details_auth_as_other_user
    @allure.description("This test ensure authorized admin user can only see other user username field. "
                        "Using default data")
    def test_get_user_details_auth_as_other_user(self):
        response_auth = MyRequests.post("/user/login", data=self.default_data)
        auth_sid = self.get_cookie(response_auth, "auth_sid")
        token = self.get_header(response_auth, "x-csrf-token")

        response_with_details = MyRequests.get(f'/user/1',
                                               headers={"x-csrf-token": token},
                                               cookies={"auth_sid": auth_sid})

        Assertions.assert_json_has_key(response_with_details, 'username')
        Assertions.assert_json_has_not_key(response_with_details, 'email')
        Assertions.assert_json_has_not_key(response_with_details, 'firstName')
        Assertions.assert_json_has_not_key(response_with_details, 'lastName')

