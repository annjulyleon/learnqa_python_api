import requests

BASE_URL = "https://playground.learnqa.ru/api"
HEADERS = {
    'User-Agent': 'Mozilla/6.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.2661.102 Safari/537.36'
}


# Note: without HEADERS second redirect returns 403 (both in homework and in lesson video)
def get_redirects(endpoint='long_redirect', redirects=True):
    response = requests.get(f"{BASE_URL}/{endpoint}", allow_redirects=redirects)
    if response.status_code == 403:
        response = requests.get(f"{BASE_URL}/{endpoint}", headers=HEADERS, allow_redirects=redirects)

    redirects = [x.url for x in response.history]
    return f'Redirects history: {redirects} \nAmount of redirects: {len(redirects)} \nLast url: {redirects[-1]} \nStatus code: {response.status_code}'


print(get_redirects())
