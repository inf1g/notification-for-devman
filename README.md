## Оповещение о проверки работ для devman.

- Скрипт выводит уведомление в windows 11 о проверке работы по уроку devman

## Установка

1. Клонируйте репозиторий с github
2. Установите зависимости 
```bash
pip install -r requirements.txt
```
3. Запустите скрипт 'devman_check.py'
```bash
python devman_check.py
```
## Настройка
1. Создайте файл .env указав имя и значение этой переменной как на примере ниже, замените 0123456789abcdefgh на свой токен с сайта https://dvmn.org/api/docs/ из графы Аутентификация.
```bash
DEVMAN_TOKEN=0123456789abcdefgh
```

### Создано с помощью 
![!Static Badge](https://img.shields.io/badge/Python-3.12-blue?style=flat-square)

