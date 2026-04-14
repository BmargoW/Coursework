import json
from src.utils import date_determination, my_list, max_sum, currency_convert, cost_shares


def views(users_data):
    try:
        one =  date_determination(users_data)
        two = my_list(users_data)
        three = max_sum(users_data)
        four = currency_convert(["USD", "EUR"])
        five = cost_shares(["AAPL"])
        data = {
        "greeting": one,
        "cards": two,
        "top_transactions": three,
        "currency_rates": four,
        "stock_prices": five
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
    #"2021-12-01 09:21:49"