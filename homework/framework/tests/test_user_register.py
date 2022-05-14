import allure
import pytest

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


@allure.epic("Registration cases")
class TestUserRegister(BaseCase):
    exclude_field = [
        "firstName",
        "lastName",
        "email",
        "username",
        "password"
    ]

    @allure.title("Cannot register with existing email")
    @allure.description("This test ensure user with existing email already exist")
    def test_create_user_with_existing_email(self):
        email = "vinkotov@example.com"
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f'Unexpected response content {response.content}'

    @pytest.mark.smoke
    @allure.title("User create")
    @allure.description("This test creates user successfully")
    @allure.story("crud")
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()
        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    #  python -m pytest -s .\tests\test_user_register.py -k test_create_user_email_without_at
    @pytest.mark.review
    @allure.title("Cannot create without @ at email")
    @allure.description("This test ensure user can't be created with email without @")
    def test_create_user_email_without_at(self):
        email = "vinkotovexample.com"
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format", \
            f'Unexpected response content {response.content}'

    # python -m pytest -s .\tests\test_user_register.py -k test_create_user_fields
    @pytest.mark.review
    @allure.title("User create without {exclude_field}")
    @allure.description("This test ensure user can't be created without one of the required field")
    @pytest.mark.parametrize('exclude_field', exclude_field)
    def test_create_user_fields(self, exclude_field):
        data = self.prepare_registration_data()
        data.pop(exclude_field, None)

        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.text == f"The following required params are missed: {exclude_field}", \
            f'Unexpected response text {response.text}'

    # python -m pytest -s .\tests\test_user_register.py -k test_create_user_with_short_field
    @pytest.mark.review
    @allure.title("User create with too short {field}")
    @allure.description("This test ensure user can't be created with too short username or firstname")
    @pytest.mark.parametrize('field', ["username", "firstName"])
    def test_create_user_with_short_field(self, field):
        data = self.prepare_registration_data()
        data[field] = 'a'

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.text == f"The value of '{field}' field is too short", \
            f'Unexpected response text {response.text}'

    # python -m pytest -s .\tests\test_user_register.py -k test_create_user_with_long_field
    @pytest.mark.review
    @allure.title("User create with too long {field}")
    @allure.description("This test ensure user can't be created with too long username or firstname")
    @pytest.mark.parametrize('field', ["username", "firstName"])
    def test_create_user_with_long_field(self, field):
        data = self.prepare_registration_data()
        data[field] = 'lqapi' * 51

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.text == f"The value of '{field}' field is too long", \
            f'Unexpected response text {response.text}'
