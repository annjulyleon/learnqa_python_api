from requests import Response
import json

class Assertions:

    @staticmethod
    def assert_json_value_by_name(response: Response, name: str, expected_value: str, error_message: str):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f'Response is not in json formats. Response text is {response.text}'

        assert name in response_as_dict, f'Response JSON does nott have key name'
        assert response_as_dict[name] == expected_value, error_message