from json.decoder import JSONDecodeError
from requests import Response
from datetime import datetime
from lib.assertions import Assertions
from lib.my_requests import MyRequests

class BaseCase:
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f'Cannot find the cookie with name {cookie_name} in the last response'

        return response.cookies[cookie_name]

    def get_header(self, response: Response, headers_name):
        assert headers_name in response.headers, f'Cannot find header with the name {headers_name} in the last response'

        return response.headers[headers_name]

    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except JSONDecodeError:
            assert False, f'Response is not in JSON Format. Response text is "{response.text}"'

        assert name in response_as_dict, f'Response JSON does not have the key "{name}"'

        return response_as_dict[name]

    def prepare_registration_data(self, email=None) -> dict:
        if email is None:
            base_part = "learnqa"
            domain = "example.com"
            random_part = datetime.now().strftime("%Y%m%d%H%M%S")
            email = f"{base_part}{random_part}@{domain}"

        return {
            "password": "123",
            "username": "learnqa",
            "firstName": "learnqa",
            "lastName": "learnqa",
            "email": email
        }

    def create_user_ensure_created(self) -> dict:
        register_data = self.prepare_registration_data()
        response_registration = MyRequests.post("/user", data=register_data)

        Assertions.assert_code_status(response_registration, 200)
        Assertions.assert_json_has_key(response_registration, "id")
        register_data["user_id"] = self.get_json_value(response_registration, "id")

        return register_data

    def get_auth_data(self, register_data: dict) -> dict:
        response_auth = MyRequests.post("/user/login",
                                        data={"email": register_data["email"],
                                              "password": register_data["password"]})
        register_data["auth_sid"] = self.get_cookie(response_auth, "auth_sid")
        register_data["token"] = self.get_header(response_auth, "x-csrf-token")
        if "user_id" not in register_data:
            register_data["user_id"] = self.get_json_value(response_auth, "user_id")

        return register_data
