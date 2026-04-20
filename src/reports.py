import datetime
import json
import logging

import pandas as pd

decor_logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("reports.log", mode="w")
file_formater = logging.Formatter("%(asctime)s %(filename)s %(funcName)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formater)
decor_logger.addHandler(file_handler)
decor_logger.setLevel(logging.INFO)


# df = pd.read_excel("../data/operations.xlsx")
# user_category = input("введите название интересущей Вас категории")
# user_date = str(input("введите дату в формате ДД-ММ-ГГГГ"))


def my_decorator(func):
    def wrapper(*arg, **kwargs):
        decor_df = func(*arg, **kwargs)
        decor_logger.info(f"траты по заданной категории за последние три месяца{decor_df}")
        return decor_df

    return wrapper


@my_decorator
def spending_by_category(transactions, category, date=None):
    """Функция возвращает траты по заданной категории за последние три месяца (от переданной даты)."""
    if date:
        date = date
    else:
        date = datetime.datetime.now()
        date = date.strftime("%d.%m.%Y")

    date_obj = datetime.datetime.strptime(date, "%d.%m.%Y")

    end_date_obj = date_obj - datetime.timedelta(days=90)

    start_date = end_date_obj
    end_date = date_obj

    transactions["Дата платежа"] = pd.to_datetime(transactions["Дата платежа"], format="%d.%m.%Y")

    mask = (
        (transactions["Дата платежа"] >= start_date)
        & (transactions["Дата платежа"] <= end_date)
        & (transactions["Категория"] == category)
    )

    category_filter = transactions[mask]

    category_filter_sum = category_filter["Сумма платежа"].sum()

    category_filter_dict = {category: round(category_filter_sum, 2)}
    json_category_filter_dict = json.dumps(category_filter_dict, ensure_ascii=False)

    return json_category_filter_dict


# if __name__ == "__main__":
#
#     print(spending_by_category(df, user_category))
