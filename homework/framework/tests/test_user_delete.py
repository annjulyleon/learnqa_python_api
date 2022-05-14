import time
import pytest
import allure
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


@allure.epic("Delete cases")
class TestUserDelete(BaseCase):
    # python -m pytest -s .\tests\test_user_delete.py -k test_user2_cannot_be_deleted
    @allure.title("User with id 2 cannot be deleted")
    @allure.description("This test ensure user 2 cannot delete itself")
    def test_user2_cannot_be_deleted(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        user = self.get_auth_data(data)
        response = MyRequests.delete(f"/user/{user['user_id']}",
                                     headers={"x-csrf-token": user["token"]},
                                     cookies={"auth_sid": user["auth_sid"]})

        Assertions.assert_code_status(response, 400)
        assert response.text == 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.', f"Incorrect message"

    # python -m pytest -s .\tests\test_user_delete.py -k test_delete_user_delete_itself
    @pytest.mark.smoke
    @allure.story("crud")
    @allure.title("User can delete itself")
    @allure.description("This test ensure authorized user can delete itself")
    def test_delete_user_delete_itself(self):
        user = self.create_user_ensure_created()
        user = self.get_auth_data(user)

        response_delete = MyRequests.delete(f"/user/{user['user_id']}",
                                            headers={"x-csrf-token": user["token"]},
                                            cookies={"auth_sid": user["auth_sid"]})
        Assertions.assert_code_status(response_delete, 200)

        response_get = MyRequests.get(f"/user/{user['user_id']}")
        Assertions.assert_code_status(response_get, 404)
        assert response_get.text == 'User not found', f'Incorrect message. Message {response_get.text}'

    # python -m pytest -s .\tests\test_user_delete.py -k test_delete_other_user
    @allure.title("User cannot delete another user")
    @allure.description("This test ensure user is not deleted after delete command of authorized user")
    def test_delete_other_user(self):
        user_auth = self.create_user_ensure_created()
        user_auth = self.get_auth_data(user_auth)

        time.sleep(2)
        user_to_delete = self.create_user_ensure_created()

        response_delete = MyRequests.delete(f"/user/{user_to_delete['user_id']}",
                                            headers={"x-csrf-token": user_auth["token"]},
                                            cookies={"auth_sid": user_auth["auth_sid"]})
        Assertions.assert_code_status(response_delete, 200)

        response_get = MyRequests.get(f"/user/{user_to_delete['user_id']}")
        Assertions.assert_code_status(response_get, 200)
        assert user_to_delete["username"] in response_get.text, \
            f'Username is either deleted or not returned in the response'
