import requests
import json

class TestCat:
    def setup(self):
        self.base_url = 'http://127.0.0.1:8090/cat'

    def test_create_cat(self):
        headers = {'content-type': 'application/json'}
        new_cat = {"name": "Krokus",
                         "gender": "male",
                         "color": "mixed",
                         "age": 3.5,
                         "description": "serious shy clever"}
        response = requests.post(f'{self.base_url}', headers=headers, data=json.dumps(new_cat))
        print(response.text)
        assert response.status_code == 201, f'Expected "201", got "{response.status_code}"'


    def test_get_cat_by_id(self):
        response = requests.get(f'{self.base_url}', params={"id": 1})
        assert response.status_code == 200, f'Expected "200", got "{response.status_code}"'

    def test_update_cat(self):
        pass

    def test_pet_cat(self):
        pass

    def test_hug_cat(self):
        pass

    def test_delete_cat(self):
        pass
