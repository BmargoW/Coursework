from src.views import views
from src.services import line_selection
from src.reports import spending_by_category
import pandas as pd


def main():

    print(
        """Программа: Привет! Добро пожаловать в программу работы
с банковскими транзакциями."""
    )
    def user_date():
        selected_date = input("Введите строку с датой и временем в формате 'YYYY-MM-DD HH:MM:SS'")
        if selected_date:
            return views(selected_date)
        else:
            return views()

    result = user_date()
    print(result)

    users_category = [str(input("По какой категории или виду операции предоставить информацию?"))]
    result_2 = line_selection(users_category)

    print(result_2)

    df = pd.read_excel("../data/operations.xlsx")
    user_category = input("Чтобы узнать траты интересующей Вас категории за последние три месяцаб введите название интересущей Вас категории")
    user_date = str(input("введите дату в формате ДД.ММ.ГГГГ"))
    result_3 = spending_by_category(df, user_category, user_date)

    print(result_3)




if __name__ == "__main__":
    main()