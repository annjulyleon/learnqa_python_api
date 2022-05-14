from json.decoder import JSONDecodeError

from requests import Response


class BaseCase():
    def get_cookie(self,response:Response, cookie_name):
        assert cookie_name in response.cookies, f'Cannot find the cookie with name {cookie_name} in the last response'

        return response.cookies[cookie_name]

    def get_header(self, response: Response, headers_name):
        assert headers_name in response.headers, f'Cannot find header with the name {headers_name} in the last response'

        return response.headers[headers_name]

    def get_json_value(self,response: Response, name):
        try:
            response_as_dict = response.json()
        except JSONDecodeError:
            assert False, f'Response is not in JSON Format, Response test is "{response.text}"'

        assert name in response_as_dict, f'Response json does no have the key "{name}"'

        return response_as_dict[name]