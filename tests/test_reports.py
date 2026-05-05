import pandas
import pytest

from src.reports import spending_by_category

data = {
    "Дата платежа": ["06.02.2021", "07.02.2021", "08.02.2021"],
    "Сумма платежа": [-138.00, 80.00, 100.00],
    "Категория": ["Супермаркеты", "Фастуфуд", "Бьюти"],
    "Описание": ["Колхоз", "ЗП", "АЗС"],
}
df = pandas.DataFrame(data)


@pytest.mark.parametrize(
    "x,y,z, expected",
    [
        (df, "Супермаркеты", "06.02.2021", '{"Супермаркеты": -138.0}'),
        (df, "Фастфуд", "07.02.2021", '{"Фастфуд": 0.0}'),
    ],
)
def test_spending_by_category(x, y, z, expected):

    assert spending_by_category(x, y, z) == expected
