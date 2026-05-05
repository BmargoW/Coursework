import json
import logging

import pandas

new_logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("utils.log", mode="w")
file_formater = logging.Formatter("%(asctime)s %(filename)s %(funcName)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formater)
new_logger.addHandler(file_handler)
new_logger.setLevel(logging.INFO)


def line_selection(designation):
    """функция возвращает JSON-ответ со всеми транзакциями, содержащими запрос, обозначенный пользователем
    в описании или категории."""

    try:
        new_logger.info("переданы корректные данные")
        excel_data = pandas.read_excel("../data/operations.xlsx")
        italy_france_reviews = excel_data.loc[
            excel_data["Категория"].isin(designation) | excel_data["Описание"].isin(designation)
        ]

        res = italy_france_reviews.to_dict(orient="records")
        json_data = json.dumps(res, ensure_ascii=False)
        print(type(json_data))
        return json_data

    except json.JSONDecodeError:
        new_logger.warning("ошибка чтения файла")
        print("invalid JSON data")
        return []

    except TypeError as e:
        new_logger.error("ошибка параметра")
        print(e)


if __name__ == "__main__":
    print(line_selection(["Супермаркеты"]))
