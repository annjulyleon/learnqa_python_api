# Some run commands

With @alure.issue link template:
```
python -m pytest --alluredir=test_results/ --allure-link-pattern=issue:'https://www.mytesttracker.com/issue/{}' .\tests
```

View report:
```
allure serve test_results/
```

Set variable from PyCharm terminal:
```
$env:ENV = 'prod'
```
View variable:
```
$env:ENV
```