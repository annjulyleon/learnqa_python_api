from requests import Response
import json
import allure


class Assertions:

    @staticmethod
    def assert_json_value_by_name(response: Response, name: str, expected_value, error_message: str):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f'Response is not in json formats. Response text is {response.text}'

        assert name in response_as_dict, f'Response JSON does not have key name'
        assert response_as_dict[name] == expected_value, error_message

    @staticmethod
    def assert_json_has_key(response: Response, name: str):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f'Response is not in json formats. Response text is {response.text}'

        assert name in response_as_dict, f'Response JSON does not have key {name}'

    @staticmethod
    def assert_json_has_not_key(response: Response, name: str):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f'Response is not in json formats. Response text is {response.text}'

        assert name not in response_as_dict, f'Response JSON should not have key {name}'

    def assert_json_has_keys(response: Response, names: list[str]):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f'Response is not in json formats. Response text is {response.text}'

        for name in names:
            assert name in response_as_dict, f'Response JSON does not have key {name}'

    @staticmethod
    def assert_code_status(response: Response, expected_status_code):
        assert response.status_code == expected_status_code, f'Unexpected status code! ' \
                                                             f'Expected: {expected_status_code},' \
                                                             f'Got: {response.status_code}'

