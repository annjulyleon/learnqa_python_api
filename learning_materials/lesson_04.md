# Allure and environments

URL: API: https://playground.learnqa.ru/api/map  
URL-DEV: API: https://playground.learnqa.ru/api_dev/map

Install allure: [installation guide](https://docs.qameta.io/allure/#_windows).  
Note: reload PyCharm to grab new PATH variables.

Command to run allure and generate reports in directory:
```
python -m pytest --alluredir=test_results/ .\tests\test_user_auth.py
```

With @alure.issue link template:
```
python -m pytest --alluredir=test_results/ --allure-link-pattern=issue:'https://www.mytesttracker.com/issue/{}' .\tests
```

View report:
```
allure serve test_results/
```

Note: logger and relative directory from lesson do not work with pycharm test launch.

Set variable from PyCharm terminal:
```
$env:ENV = 'prod'
```
View variable:
```
$env:ENV
```

In docker set timezone:
```
ENV TZ=Europe/Moscow
```

Run docker build:

```
docker build -t pytest_runner .
```

Run docker:
```
docker run --rm --mount type=bind,src=D:\virtualenv\learnqa_python_api\homework\framework,target=/tests_projects/ pytest_runner

```

With docker-compose:
```
docker-compose up --build
```