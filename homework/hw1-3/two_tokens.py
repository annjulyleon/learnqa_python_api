import requests
import time

BASE_URL = "https://playground.learnqa.ru/ajax/api/longtime_job"


def create_task() -> dict:
    response = requests.get(BASE_URL).json()

    return response


def get_status(token) -> dict:
    response = requests.get(BASE_URL,params={"token":token}).json()

    return response


# script to get and check token
def check_task_creation():
    created_task = create_task()
    print(f'Created task with token: {created_task.get("token")}, time: {created_task.get("seconds")}')

    checked_task = get_status(created_task.get("token"))

    if checked_task.get("error"):
        print(checked_task.get("error"))
    else:
        print(
            f'Checked status of the task with token {created_task.get("token")}. Status: {checked_task.get("status")}')
        time.sleep(created_task.get("seconds"))
        result = get_status(created_task.get("token"))

        if result.get("result") and result.get("status") == 'Job is ready':
            print(f'Jobe is done! Result is: {result.get("result")}. Status is: {result.get("status")}')
        else:
            print(f'Job is not ready or some terrible thing happened and result is not provided! Hnik Hnik!')


check_task_creation()
