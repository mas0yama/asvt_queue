# Запуск:
1. Открыть проект в IDE
2. Создать виртуальное окружение `venv` (способ зависит от платформы и IDE)
3. Установить все пакеты из файла `requirements.txt` (`pip install -r requirements.txt` или `pip install <package==version>` для каждого пакета)
4. Создать в корне проекта файл `.env`, вписать туда `APP_KEY=<secret key>`
5. Вписать в `.env` `PICTURES_STORAGE=<path>` - путь к папке, где будут храниться все фото 
6. Выполнить `cd r_queue`
7. Выполнить `python manage.py migrate`
8. Выполнить `python manage.py createsuperuser`, ввести желаемые логин и пароль, почту (логин и пароль требуется запомнить)
9. Выполнить `python manage.py runserver`. Он будет иметь адрес по умолчанию: http://127.0.0.1:8000
10. Для запуска сервера в локальной сети в файле `r_queue/r_queue/settings.py` изменить значение переменной `PUBLIC` на `True`, запустить командой `python manage.py runserver 0.0.0.0:8000`

# Доступ к странице менеджера:
1. Ввести в адресной строке http://127.0.0.1:8000/login 
2. Ввести в адресной строке http://127.0.0.1:8000/manager_panel/
