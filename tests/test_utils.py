from unittest.mock import mock_open, patch

import pandas
import pytest

from src.utils import (cost_shares, currency_convert, date_determination,
                       max_sum, my_list, uploading_content)


def test_date_determination_user():
    assert date_determination("2021-12-25 22:21:49") == "доброй ночи"
    assert date_determination("2021-12-25 12:21:49") == "добрый день"
    assert date_determination("2020-03-25 09:21:49") == "доброе утро"

    with pytest.raises(TypeError):
        date_determination(1)

    with pytest.raises(NameError):
        date_determination(s)


def test_my_list():
    mock_data = {
        "Дата платежа": ["01.12.2021"],
        "Номер карты": ["*7197"],
        "Сумма платежа": ["169"],
        "Кэшбэк": [3],
    }
    df = pandas.DataFrame(mock_data)

    with patch("pandas.read_excel") as mock_read_excel:
        mock_read_excel.return_value = df
        assert my_list("2021-12-01 09:21:49") == [
            {"last_digits": "7197", "total_spent": 169, "cashback": 3}
        ]


def test_max_sum():

    mock_df = pandas.DataFrame(
        {
            "Дата платежа": [
                "01.12.2021",
                "02.12.2021",
                "03.12.2021",
                "04.12.2021",
                "05.12.2021",
                "07.12.2021",
                "06.12.2021",
            ],
            "Категория": [
                "супермаркет",
                "кафе",
                "АЗС",
                "автомойка",
                "салон",
                "кино",
                "театр",
            ],
            "Описание": [
                "доход 1",
                "доход 2",
                "доход 3",
                "доход 4",
                "доход 5",
                "доход 6",
                "доход 7",
            ],
            "Сумма платежа": [300, 50, 1000, 10, 1, 20000, 700],
        }
    )

    with patch("pandas.read_excel") as mock_read_excel:
        mock_read_excel.return_value = mock_df
        assert (
            max_sum("2021-12-07 09:21:49")
            == [
                {
                    "amount": 20000.0,
                    "category": "кино",
                    "date": "2021-12-07 00:00:00",
                    "description": "доход 6",
                },
                {
                    "amount": 1000.0,
                    "category": "АЗС",
                    "date": "2021-12-03 00:00:00",
                    "description": "доход 3",
                },
                {
                    "amount": 700.0,
                    "category": "театр",
                    "date": "2021-12-06 00:00:00",
                    "description": "доход 7",
                },
                {
                    "amount": 300.0,
                    "category": "супермаркет",
                    "date": "2021-12-01 00:00:00",
                    "description": "доход 1",
                },
                {
                    "amount": 50.0,
                    "category": "кафе",
                    "date": "2021-12-02 00:00:00",
                    "description": "доход 2",
                },
            ]
            != [
                {
                    "amount": 300.0,
                    "category": "супермаркет",
                    "date": "2021-12-01 00:00:00",
                    "description": "доход 1",
                }
            ]
        )


def test_currency_convert():
    js_data = {
        "success": True,
        "query": {"from": "USD", "to": "RUB", "amount": 1},
        "info": {"timestamp": 1775260985, "rate": 80.325739},
        "date": "2026-04-04",
        "result": 80.325739,
    }

    with patch("requests.request") as mock_response:
        mock_response.return_value.json.return_value = js_data
        my_list = ["USD"]
        assert currency_convert(my_list) == [{"currency": "USD", "rate": 80.33}]


def test_uploading_content_valid_json():
    test_data = '{"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL"]}'
    m = mock_open(read_data=test_data)
    with patch("builtins.open", m):
        result = uploading_content("dummy.json")
        assert result == ["USD", "EUR"]


def test_cost_shares():
    js_data = {
        "Meta Data": {
            "1. Information": "Monthly Adjusted Prices and Volumes",
            "2. Symbol": "AAPL",
            "3. Last Refreshed": "2026-03-31",
            "4. Time Zone": "US/Eastern",
        },
        "Monthly Adjusted Time Series": {
            "2026-03-31": {
                "1. open": "262.4100",
                "2. high": "266.5300",
                "3. low": "245.5100",
                "4. close": "253.7900",
                "5. adjusted close": "253.7900",
                "6. volume": "900035757",
                "7. dividend amount": "0.0000",
            }
        },
    }

    with patch("requests.get") as mock_response:
        mock_response.return_value.json.return_value = js_data
        my_list = ["AAPL"]
        assert cost_shares(my_list) == [{"stock": "AAPL", "rate": 253.79}]
