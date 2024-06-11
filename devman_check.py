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
    print(status)
    response = requests.get(url, headers=headers, params=status)
    response.raise_for_status()
    print(response.json())
    return response.json()


def check_status(json):
    if json['status'] == 'timeout':
        print(json['timestamp_to_request'])
        return json['timestamp_to_request']
    else:
        print(json['status'])
        return json['status']


def alert(name):
    toast('DEVMAN', 'Ответ по решению урока 🐦',
          audio='ms-winsoundevent:Notification.Looping.Alarm3',
          on_click=f'https://dvmn.org/works/author/{name}/'
          )


def main():
    token = configure_keys("DEVMAN_TOKEN")
    nick_name = configure_keys("NICK")
    status = check_status(get_response(token))
    while True:
        if status == "found":
            alert(nick_name)
            break
        else:
            print("False")
            timestamp = {"timestamp": status}
            status = check_status(get_response(token, timestamp))
            continue


if __name__ == '__main__':
    main()
