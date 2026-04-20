import json
import datetime
from src.utils import cost_shares, currency_convert, date_determination, max_sum, my_list


def views(users_data=None):

    if users_data:
        u_data = users_data
    else:
        now_data = datetime.datetime.now()
        u_data = now_data.strftime("%Y-%m-%d %H:%M:%S")
    try:
        one = date_determination(u_data)
        two = my_list(u_data)
        three = max_sum(u_data)
        four = currency_convert(["USD", "EUR"])
        five = cost_shares(["AAPL"])
        data = {
            "greeting": one,
            "cards": two,
            "top_transactions": three,
            "currency_rates": four,
            "stock_prices": five,
        }

        json_data = json.dumps(data, ensure_ascii=False, indent=4)
        return json_data

    except ValueError:
        print("""Ошибка. Неверный формат ввода. Введите строку с датой и временем в формате
              'YYYY-MM-DD HH:MM:SS'""")


if __name__ == "__main__":
    users_input = input("""Введите строку с датой и временем в формате
              "YYYY-MM-DD HH:MM:SS" """)
    print(views(users_input))
    # print(data)
    # print(json_data)
    # "2021-12-01 09:21:49"
