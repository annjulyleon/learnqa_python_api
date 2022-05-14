import time

import allure
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


@allure.epic("User edit cases")
class TestUserEdit(BaseCase):
    @pytest.mark.smoke
    @allure.story("crud")
    @allure.title("Edit created user")
    @allure.description("This test ensure user can edit its own details")
    def test_edit_just_created_user(self):
        register_data = self.prepare_registration_data()
        response_registration = MyRequests.post("/user", data=register_data)

        Assertions.assert_code_status(response_registration, 200)
        Assertions.assert_json_has_key(response_registration, "id")

        email = register_data['email']
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

    # python -m pytest -s .\tests\test_user_edit.py -k test_edit_created_user_unauth
    @allure.title("Unauth user cannot edit {field}")
    @allure.description("This test ensure unauthorized user can't edit it's own details")
    @pytest.mark.parametrize('field', ["username", "firstName", "lastName", "email", "password"])
    def test_edit_created_user_unauth(self, field):
        user_data = self.create_user_ensure_created()
        new_value = 'new' + user_data[field]

        response_change = MyRequests.put(f"/user/{user_data['user_id']}", data={field: new_value})
        Assertions.assert_code_status(response_change, 400)
        assert response_change.text == f"Auth token not supplied", \
            f'Unexpected response text {response_change.text}'

    # python -m pytest -s .\tests\test_user_edit.py -k test_edit_other_user_auth
    @allure.title("Unauth user cannot edit {field} of other user")
    @allure.description("This test ensure authorized user can edit other user details, but details are not changed")
    @pytest.mark.parametrize('field', ["username", "firstName", "lastName", "email", "password"])
    def test_edit_other_user_auth(self, field):
        user_auth = self.create_user_ensure_created()
        user_auth = self.get_auth_data(user_auth)

        time.sleep(2)
        user_to_edit = self.create_user_ensure_created()
        user_to_edit = self.get_auth_data(user_to_edit)
        new_value = 'new' + user_to_edit[field]

        response_change = MyRequests.put(f"/user/{user_to_edit['user_id']}",
                                         headers={"x-csrf-token": user_auth["token"]},
                                         cookies={"auth_sid": user_auth["auth_sid"]},
                                         data={field: new_value})
        Assertions.assert_code_status(response_change, 200)

        response_get = MyRequests.get(f"/user/{user_to_edit['user_id']}",
                                      headers={"x-csrf-token": user_to_edit["token"]},
                                      cookies={"auth_sid": user_to_edit["auth_sid"]})
        if field == 'password':
            response_try_auth = MyRequests.post("/user/login",
                                                data={"email": user_to_edit["email"],
                                                      "password": new_value})
            Assertions.assert_code_status(response_try_auth, 400)
            assert response_try_auth.text == 'Invalid username/password supplied', \
                f'Was able to login with changed password {new_value}'
        else:
            Assertions.assert_json_value_by_name(
                response_get,
                field,
                user_to_edit[field],
                f"Value of the '{field}' was changed to '{new_value}' incorrectly. "
                f"Value should not be changed by other user")

    # python -m pytest -s .\tests\test_user_edit.py -k test_edit_auth_user_email_format
    @allure.title("User can't remove @ from email")
    @allure.description("This test ensure authorized user can't edit it's own email to incorrect format")
    def test_edit_auth_user_email_format(self):
        user = self.create_user_ensure_created()
        user = self.get_auth_data(user)
        new_value = 'emailwithoutat.com'

        response_change = MyRequests.put(f"/user/{user['user_id']}",
                                         headers={"x-csrf-token": user["token"]},
                                         cookies={"auth_sid": user["auth_sid"]},
                                         data={"email": new_value})

        Assertions.assert_code_status(response_change, 400)
        assert response_change.text == 'Invalid email format', \
            f'Was able to change email to incorrect format {new_value}' \
            f' or got other error {response_change.text}'

    # python -m pytest -s .\tests\test_user_edit.py -k test_edit_auth_user_firstname_short
    @allure.title("User can't put too short firstName")
    @allure.description("This test ensure authorized user can't edit it's own firstName to incorrect format")
    def test_edit_auth_user_firstname_short(self):
        user = self.create_user_ensure_created()
        user = self.get_auth_data(user)
        new_value = 'b'

        response_change = MyRequests.put(f"/user/{user['user_id']}",
                                         headers={"x-csrf-token": user["token"]},
                                         cookies={"auth_sid": user["auth_sid"]},
                                         data={"firstName": new_value})

        Assertions.assert_code_status(response_change, 400)
        assert response_change.text == '{"error":"Too short value for field firstName"}', \
            f'Was able to change firstName to incorrect format {new_value} or got other error {response_change.text}'
