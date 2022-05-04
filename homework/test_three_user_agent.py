import requests
import pytest
import pytest_check as check

''' 
python -m pytest -v .\test_three_user_agent.py

Expected:
FAILED test_three_user_agent.py::test_user_agent_method[user_agent1] - AssertionError: For user-agent ios: browser "No" does not match expected result (Chrome)
FAILED test_three_user_agent.py::test_user_agent_method[user_agent2] - AssertionError: For user-agent unknown: platform "Unknown" does not match expected result (Googlebot)
FAILED test_three_user_agent.py::test_user_agent_method[user_agent4] - AssertionError: For user-agent iphone: device "Unknown" does not match expected result (iPhone)
'''

user_agents = {
    'android': 'Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
    'ios':'Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1',
    'unknown':'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'no':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0',
    'iphone':'Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
}

expected_results = {
    'android': {'platform': 'Mobile', 'browser': 'No', 'device': 'Android'},
    'ios': {'platform': 'Mobile', 'browser': 'Chrome', 'device': 'iOS'},
    'unknown':{'platform': 'Googlebot', 'browser': 'Unknown', 'device': 'Unknown'},
    'no':{'platform': 'Web', 'browser': 'Chrome', 'device': 'No'},
    'iphone': {'platform': 'Mobile', 'browser': 'No', 'device': 'iPhone'}

}


@pytest.mark.parametrize('user_agent',user_agents.items())
def test_user_agent_method(user_agent):
    response = requests.get('https://playground.learnqa.ru/ajax/api/user_agent_check',
                            headers={'User-agent': user_agent[1]})
    response_json = response.json()
    expected = expected_results[user_agent[0]]

    platform = response_json['platform']
    browser = response_json['browser']
    device = response_json['device']

    '''
    This will fail on first assert fail
    assert platform == expected['platform'], \
        f'For user-agent {user_agent[0]}: platform "{platform}" does not match expected result ({expected["platform"]})'
    assert browser == expected['browser'], \
        f'For user-agent {user_agent[0]}: browser "{browser}" does not match expected result ({expected["browser"]})'
    assert device == expected['device'], \
        f'For user-agent {user_agent[0]}: device "{device}" does not match expected result ({expected["device"]})'
    '''

    # this will not fail on first assert
    check.equal(platform, expected['platform']), f'For user-agent {user_agent[0]}: platform "{platform}" does not match expected result ({expected["platform"]})'
    check.equal(browser, expected['browser']), f'For user-agent {user_agent[0]}: browser "{browser}" does not match expected result ({expected["browser"]})'
    check.equal(device,expected['device']), f'For user-agent {user_agent[0]}: device "{device}" does not match expected result ({expected["device"]})'