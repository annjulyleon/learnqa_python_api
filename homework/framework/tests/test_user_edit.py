import requests

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        register_data = self.prepare_registration_data()
        response_registration = MyRequests.post("/user", data=register_data)

        Assertions.assert_code_status(response_registration, 200)
        Assertions.assert_json_has_key(response_registration, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        last_name = register_data['lastName']
        password = register_data['password']
        user_id = self.get_json_value(response_registration, "id")

        login_data = {
            "email": email,
            "password": password
        }

        response_auth = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response_auth, "auth_sid")
        token = self.get_header(response_auth, "x-csrf-token")

        new_name = "Changed Name"

        response_change = MyRequests.put(f"/user/{user_id}",
                                       headers={"x-csrf-token": token},
                                       cookies={"auth_sid": auth_sid},
                                       data={"firstName": new_name})

        Assertions.assert_code_status(response_change, 200)

        response_check_name = MyRequests.get(f"/user/{user_id}",
                                       headers={"x-csrf-token": token},
                                       cookies={"auth_sid": auth_sid})

        Assertions.assert_json_value_by_name(response_check_name,
                                             "firstName",
                                             new_name,
                                             "Wrong firstName after edit")