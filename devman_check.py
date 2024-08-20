import requests
import os
from dotenv import load_dotenv
from win11toast import toast


def configure_keys(token):
    load_dotenv()
    key = os.getenv(token)
    return key


def get_response(token, status=None):
    url = "https://dvmn.org/api/long_polling/"
    headers = {
        'Authorization': f'Token {token}'
    }
    response = requests.get(url, headers=headers, params=status)
    response.raise_for_status()
    return response.json()


def check_status(response):
    if response['status'] == 'timeout':
        return response['timestamp_to_request']
    else:
        return response['status'], response["new_attempts"][0]["is_negative"], response["new_attempts"][0]["lesson_url"]


def alert(is_negative, lesson_url):
    if is_negative:
        answer = 'Нет'
    else:
        answer = 'Да'
    toast('DEVMAN', f'Ответ по решению урока 🐦 Урок сдан {answer}',
          audio='ms-winsoundevent:Notification.Looping.Alarm3',
          on_click=lesson_url
          )


def main():
    token = configure_keys("DEVMAN_TOKEN")
    status, is_negative, lesson_url = check_status(get_response(token))
    while True:
        if status == "found":
            alert(is_negative, lesson_url)
            break
        else:
            timestamp = {"timestamp": status}
            status = check_status(get_response(token, timestamp))
            continue


if __name__ == '__main__':
    main()
