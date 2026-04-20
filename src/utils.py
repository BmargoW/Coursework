import datetime
import json
import logging
import os

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

app_logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("utils.log", mode="w")
file_formater = logging.Formatter("%(asctime)s %(filename)s %(funcName)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formater)
app_logger.addHandler(file_handler)
app_logger.setLevel(logging.INFO)
# stream_handler = logging.StreamHandler()
# stream_handler.setFormatter(file_formater)
# app_logger.addHandler(stream_handler)


def date_determination(data_user):
    """функция, которая принимает строку с датой и временем и возвращает приветствие,
    если ничего не получает на вход то использует настоящую дату и время"""
    try:
        if data_user:
            app_logger.info("дата введена пользователем")
            data_obj = datetime.datetime.strptime(data_user, "%Y-%m-%d %H:%M:%S")
            hour = data_obj.hour
            if hour < 12:
                return "доброе утро"
            elif 12 <= hour < 18:
                return "добрый день"
            elif 18 <= hour < 21:
                return "добрый вечер"
            else:
                return "доброй ночи"
        else:
            app_logger.info("дата не введена пользователем")
    except ValueError:
        app_logger.warning("дата введена некорректно")
        print("""Ошибка. Неверный формат ввода. Введите строку с датой и временем в формате
              'YYYY-MM-DD HH:MM:SS'""")


def my_list(date_of_the_month):
    """функция, которая принимает на вход дату, в зависимоти от которой
    устанавливает диапозон для анализа данных, хранящихся в файле, с начала месяца"""

    df = pd.read_excel("../data/operations.xlsx")
    date_obj = datetime.datetime.strptime(date_of_the_month, "%Y-%m-%d %H:%M:%S")

    start_of_month = date_obj.replace(day=1)
    end_date_datetime = date_obj.strftime("%d.%m.%Y")
    end_date = date_obj.strptime(end_date_datetime, "%d.%m.%Y")
    start_datetime = start_of_month.strftime("%d.%m.%Y")
    start_date = date_obj.strptime(start_datetime, "%d.%m.%Y")

    df["Дата платежа"] = pd.to_datetime(df["Дата платежа"], format="%d.%m.%Y")

    a = df[(df["Дата платежа"] >= start_date) & (df["Дата платежа"] <= end_date)]
    app_logger.info(f"определен период{a}")
    costems = []
    for index, row in a.iterrows():
        list_1 = {
            "last_digits": str(row["Номер карты"])[-4:],
            "total_spent": float(row["Сумма платежа"]),
            "cashback": float(row["Кэшбэк"]),
        }
        costems.append(list_1)
    # print(end_date_datetime, start_datetime)
    return costems


def max_sum(date_of_the_month):
    """функция, которая принимает дату, и в заданном диапозоне выбирает 5 максимальных операций"""
    df = pd.read_excel("../data/operations.xlsx")
    date_obj = datetime.datetime.strptime(date_of_the_month, "%Y-%m-%d %H:%M:%S")

    start_of_month = date_obj.replace(day=1)
    end_date_datetime = date_obj.strftime("%d.%m.%Y")
    end_date = date_obj.strptime(end_date_datetime, "%d.%m.%Y")
    start_datetime = start_of_month.strftime("%d.%m.%Y")
    start_date = date_obj.strptime(start_datetime, "%d.%m.%Y")

    df["Дата платежа"] = pd.to_datetime(df["Дата платежа"], format="%d.%m.%Y")

    a = df[(df["Дата платежа"] >= start_date) & (df["Дата платежа"] <= end_date)]

    sorted_by_summa = a.sort_values(by=["Сумма платежа"], ascending=False)
    selection = []
    for index, row in sorted_by_summa.head(5).iterrows():
        list_2 = {
            "date": str(row["Дата платежа"]),
            "amount": float(row["Сумма платежа"]),
            "category": str(row["Категория"]),
            "description": str(row["Описание"]),
        }
        selection.append(list_2)
    return selection


def currency_convert(list_c):
    """Функция, которая принимает вид валюты и вовзращает курс в рублях"""
    list_currency = []

    for i in list_c:
        API_KEY = os.getenv("API_KEY")
        url = f"https://api.apilayer.com/fixer/convert?to=RUB&from={i}&amount={1}"
        payload = {}
        headers = {"apikey": API_KEY}

        try:
            app_logger.info("запрос выполнен")
            response = requests.request("GET", url, headers=headers, data=payload)
            result = response.json()
            currency_rate = round(float(result["info"]["rate"]), 2)
            list_currency.append({"currency": i, "rate": currency_rate})

        except Exception as e:
            app_logger.error(f"Непредвиденная ошибка при обработке валюты {e}")
    return list_currency


def cost_shares(my_list):
    """функция, которая принимает наименования акций и возвращает их стоимость"""

    list_currency = []

    for i in my_list:
        API_KEY = os.getenv("API_KEY_2")
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={i}&apikey={API_KEY}"
        response = requests.get(url)
        result_1 = response.json()
        a = result_1["Meta Data"]["3. Last Refreshed"]
        cost_1 = round(float(result_1["Monthly Adjusted Time Series"][a]["4. close"]), 2)
        list_currency.append({"stock": i, "rate": cost_1})

    return list_currency


def uploading_content(name_file):
    """функция из JSON-файла возвращает список  с данными о видах валюты и акций."""
    with open(name_file, encoding="utf-8") as json_file:
        try:
            data = json.load(json_file)
            return data["user_currencies"]
        except json.JSONDecodeError:
            print("invalid JSON data")
            return []


if __name__ == "__main__":
    # data_str = input(str("введите дату в формате YYYY-MM-DD HH:MM:SS"))
    print(currency_convert(["USD", "EUR"]))

# ValueError: time data ' 2022-04-23 23:15:00' does not match format '%Y-%m-%d %H:%M:%S'
# "25.12.2021 22:21:49" 2021-12-25 22:21:49
