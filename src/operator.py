import os
import subprocess

import requests
import streamlit as st
import pandas as pd
from datetime import datetime

SERVER = "0.0.0.0:8000"


# Функция генерации нового талона
def generate_ticket(current_ticket):
    letter = current_ticket[0]  # Первая буква
    number = int(current_ticket[1:])  # Число

    # Логика увеличения номера талона
    if number < 99:
        number += 1
    else:
        number = 0
        letter = chr(ord(letter) + 1)  # Следующая буква

    return f"{letter}{str(number).zfill(2)}"


# Функция для отображения заголовка и описания страницы
def render_page_header(title):
    st.markdown(f"<h1 style='text-align: center;'>{title}</h1>", unsafe_allow_html=True)


# Функция для получения/инициализации состояния
def get_or_initialize_state(key, default_value):
    if key not in st.session_state:
        st.session_state[key] = default_value
    return st.session_state[key]


# Страница: Список талонов и кабинетов
def page_ticket_list():
    render_page_header("Список талонов и кабинетов")

    current_time = datetime.now()  # Получаем текущее время
    st.markdown(
        f"<h2 style='font-size: 30px; color: black;'>Дата и время: <strong>{current_time.strftime('%Y-%m-%d %H:%M:%S')}</strong></h2>",
        unsafe_allow_html=True)

    # Инициализация списка талонов, если он еще не существует
    if 'ticket_list' not in st.session_state:
        st.session_state['ticket_list'] = []

    # Пример данных (динамическое добавление кабинета)
    if len(st.session_state['ticket_list']) == 0:
        st.write("Талоны еще не выданы.")
    else:
        data = {
            "Номер талона": st.session_state['ticket_list'],
            "Кабинет": ["1"] * len(st.session_state['ticket_list'])  # Все талоны относятся к одному кабинету
        }
        df = pd.DataFrame(data)
        st.table(df)


# Страница: Оператор
def page_operator():
    render_page_header("Страница оператора")

    # Инициализация состояния для оператора
    ticket = get_or_initialize_state("operator_ticket", "A00")

    # Показ текущего талона
    st.write(f"Текущий клиент: **{ticket}**")

    # Кнопка переключения на следующего клиента
    if st.button("Следующий клиент"):
        new_ticket = generate_ticket(ticket)  # Генерация следующего талона
        st.session_state["operator_ticket"] = new_ticket  # Обновление текущего талона для оператора
        st.session_state["current_ticket"] = new_ticket  # Обновление текущего талона для выдачи
        st.success(f"Переключаемся на следующего клиента: **{new_ticket}**")

        # Добавление нового талона в список талонов (только после того как был получен талон на странице 'Клиент')
        if 'ticket_list' not in st.session_state:
            st.session_state['ticket_list'] = []

        # Если талон был сгенерирован на странице "Клиент", добавляем его в список
        if 'current_ticket' in st.session_state and st.session_state['current_ticket'] != "A00":
            st.session_state['ticket_list'].append(st.session_state['current_ticket'])
        else:
            st.warning("Талон не был выдан. Пожалуйста, сначала получите талон на странице 'Клиент'.")


# Страница: Выдача талонов
def page_ticket_issue():
    render_page_header("Выдача талонов")

    # Инициализация состояния для выдачи талонов
    ticket = get_or_initialize_state("current_ticket", "A00")

    # Кнопка получения нового талона
    if st.button("Получить новый талон"):
        new_ticket = generate_ticket(ticket)
        try:
            r = subprocess.run(
                f"libcamera-still --encoding jpg -o {new_ticket}.jpg  --nopreview --width 640 --height 480")
            if r.returncode == 0:
                try:
                    resp = requests.post(SERVER + "/addToQueue?tag=5", files={'file': open(new_ticket, "rb")})
                    if resp.status_code == 200:
                        st.session_state["current_ticket"] = new_ticket
                        st.markdown(
                            f"<h2 style='font-size: 30px; color: green;'>Ваш новый талон: <strong>{new_ticket}</strong></h2>",
                            unsafe_allow_html=True)
                        return
                except Exception as e:
                    print(e)
        except Exception as e:
            st.markdown(
                f"<h2 style='font-size: 30px; color: red;'>Не удалось выдать талон<strong>{new_ticket}</strong></h2>",
                unsafe_allow_html=True)

        # Не добавляем новый талон в список на этой странице!


# Главная функция
def main():
    # Боковая панель навигации
    st.sidebar.title("Навигация")
    pages = {
        "Список талонов и кабинетов": page_ticket_list,
        "Страница оператора": page_operator,
        "Выдача талонов": page_ticket_issue
    }
    choice = st.sidebar.radio("Выберите страницу:", list(pages.keys()))

    # Отображение выбранной страницы
    pages[choice]()


# Запуск приложения
if __name__ == "__main__":
    main()
