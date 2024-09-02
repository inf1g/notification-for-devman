import requests
import os
from dotenv import load_dotenv
from win11toast import toast


def configure_keys(token_name):
    load_dotenv()
    return os.getenv(token_name)


def get_response(token, status=None):
    url = "https://dvmn.org/api/long_polling/"
    headers = {'Authorization': f'Token {token}'}
    response = requests.get(url, headers=headers, params=status)
    response.raise_for_status()
    return response.json()


def check_status(response):
    if response['status'] == 'timeout':
        return response['timestamp_to_request'], None, None
    else:
        attempt = response["new_attempts"][0]
        return response['status'], attempt["is_negative"], attempt["lesson_url"]


def alert(is_negative, lesson_url):
    answer = 'Нет' if is_negative else 'Да'
    toast(
        'DEVMAN',
        f'Ответ по решению урока 🐦 Урок сдан?: {answer}',
        audio='ms-winsoundevent:Notification.Looping.Alarm3',
        on_click=lesson_url
    )


def main():
    token = configure_keys("DEVMAN_TOKEN")
    status, is_negative, lesson_url = None, None, None

    while True:
        response = get_response(token, {"timestamp": status} if status else None)
        status, is_negative, lesson_url = check_status(response)

        if status == "found":
            alert(is_negative, lesson_url)
            break


if __name__ == '__main__':
    main()
